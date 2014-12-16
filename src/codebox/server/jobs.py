import json, time, uuid

from concurrent.futures import ThreadPoolExecutor, Future
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
from tornado.gen import coroutine
from codebox.sandbox.picker import pick_sandbox, guess_sandbox

JOBS = {}
EXECUTOR = ThreadPoolExecutor(max_workers=4)

def run_sandbox(sandbox):
    result = sandbox.run()
    sandbox.destroy()
    return result

def build_sandbox(job_id, filename, source, sbtype=None): 
    if not sbtype:
        sbtype = guess_sandbox(filename)

    sb_cls = pick_sandbox(sbtype)
    sandbox = sb_cls(filename, codesource=source)
    sandbox.build()
    
    future = EXECUTOR.submit(run_sandbox, sandbox)
    JOBS[job_id]['stage'] = 'run'
    JOBS[job_id]['run_future'] = future

    return "Success."

class NewJobHandler(RequestHandler):
    def post(self):
        filename = self.get_argument('filename', None)
        source = self.get_argument('source', None)
        sbtype = self.get_argument('sbtype', None)
        if not (source and filename):
            if 'upload' not in self.request.files:
                self.set_status(400)
                return
            filename = self.request.files['upload'][0]['filename']
            source = self.request.files['upload'][0]['body']
        
        job_id = uuid.uuid4().hex
        future = EXECUTOR.submit(build_sandbox, job_id, filename, source, sbtype=sbtype)
        JOBS[job_id] = {'stage': 'build',
                        'build_future': future,
                        'run_future': None,
                        }

        response = {'job_id': job_id}
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response))

class GetJobHandler(RequestHandler):
    def get(self, job_id):
        if job_id not in JOBS:
            self.set_status(404)
            return
        job = JOBS[job_id]
        result = {
            'job_id': job_id,
            'stage': job['stage'],
            'build_done': job['build_future'].done(),
            'build_running': job['build_future'].running(),
            'build_exception': None,
            'build_result': None,
            'run_done': None,
            'run_running': None,
            'run_exception': None,
            'run_result': None,
            }
        if job['build_future'].done():
            result['build_exception'] = job['build_future'].exception()
            if not result['build_exception']:
                result['build_result'] = str(job['build_future'].result())
            else:
                result['build_exception'] = str(result['build_exception'])
        if job['stage'] == 'run':
            result['run_done'] = job['run_future'].done()
            result['run_running'] = job['run_future'].running()
            result['run_exception'] = job['run_future'].exception()
            if not result['run_exception']:
                result['run_result'] = job['run_future'].result()
                if type(result['run_result'])==bytes:
                    result['run_result'] = result['run_result'].decode()
            else:
                result['run_exception'] = str(result['run_exception'])

        self.set_header("Content-Type", "application/json")
        print(result)
        self.write(json.dumps(result))
