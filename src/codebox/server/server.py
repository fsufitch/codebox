from tornado.web import Application
from tornado.ioloop import IOLoop

from yaul.daemon import Daemon, run_as_service

from codebox.server.jobs import NewJobHandler, GetJobHandler

PATHS = [
         (r'/job/new', NewJobHandler),
         (r'/job/get/(.*)', GetJobHandler),
         ]
        
def run_server():
    webapp = Application(PATHS)
    webapp.listen(9000)
    print("Listening on port 9000...")
    IOLoop.instance().start()

class CodeBoxApiDaemon(Daemon):
    def run(self):
        run_server()

def main_service():
    run_as_service(CodeBoxApiDaemon('/tmp/codebox.pid'))

def main_cli():
    run_server()

