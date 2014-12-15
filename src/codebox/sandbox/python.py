import os, shutil
from codebox.sandbox.sandbox import GenericSandbox

DOCKERFILE_EXTRA = '''
RUN apt-get install -y python
RUN mkdir /sandbox
WORKDIR /sandbox
'''

class PythonSandbox(GenericSandbox):
    def __init__(self, codepath):
        super(PythonSandbox, self).__init__()

        self.codepath = os.path.realpath(codepath)
        self.srcname = os.path.split(codepath)[1]
        self.sympath = os.path.join(self.dockerdir, self.srcname)

        os.chdir(self.dockerdir)
        #os.symlink(self.codepath, self.sympath)
        shutil.copyfile(self.codepath, self.sympath)
        print(os.getcwd())

        self.image_tag = 'codebox/python'
        
        self.dockerfile += DOCKERFILE_EXTRA
        self.dockerfile += "ADD %s /sandbox/%s" % (self.srcname, self.srcname)

    def run(self):
        command = ['python', self.srcname]
        return self.run_cmd(command)
