import os, shutil
from codebox.sandbox.sandbox import GenericSandbox

class PythonSandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None, client_args={}):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        super(PythonSandbox, self).__init__(client_args=client_args)
        self.dockerfile.append("RUN apt-get install -y python3")

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        self.image_tag = 'codebox/python3'

    def run(self, *args, **kwargs):
        command = ['python3', self.srcname]
        return self.run_cmd(command, *args, **kwargs)

class LegacyPythonSandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None, client_args={}):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        super(LegacyPythonSandbox, self).__init__(client_args=client_args)
        self.dockerfile.append("RUN apt-get install -y python2.7")

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        self.image_tag = 'codebox/python2_7'

    def run(self, *args, **kwargs):
        command = ['python2.7', self.srcname]
        return self.run_cmd(command, *args, **kwargs)
    
