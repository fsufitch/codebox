import json, os, shutil, tempfile
from io import BytesIO
from docker import Client

BASE_DOCKERFILE = '''
FROM ubuntu
RUN echo "hello world"
'''

class GenericSandbox(object):
    def __init__(self):
        self.client = Client()
        self.dockerfile = BASE_DOCKERFILE
        self.dockerdir = tempfile.mkdtemp('codebox_docker')
        self.image_tag = 'codebox/generic'
        self.built = False

    def build(self):
        dockerpath = os.path.join(self.dockerdir, 'Dockerfile')
        with open(dockerpath, 'w') as f:
            print(self.dockerfile)
            f.write(self.dockerfile)
        buildresult = self.client.build(path=self.dockerdir,
                                        tag=self.image_tag,
                                        )
        for row in buildresult:
            row = json.loads(row)
            if row.get('error'):
                raise Exception('Image building error', row)
        self.built = True

    def run_cmd(self, command):
        assert self.built
        container = self.client.create_container(image=self.image_tag,
                                                 command=command,
                                                 mem_limit="100m",)
        cid = container['Id']
        self.client.start(container=cid)
        self.client.wait(container=cid)
        logs = self.client.logs(container=cid)
        self.client.remove_container(container=cid)
        return logs
        

    def destroy(self):
        shutil.rmtree(self.dockerdir)
            
