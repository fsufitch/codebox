import os, shutil
from codebox.sandbox.sandbox import GenericSandbox

class PHP5Sandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None, client_args={}):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        super(PHP5Sandbox, self).__init__(client_args=client_args)
        self.dockerfile.append("RUN apt-get update")
        self.dockerfile.append("RUN apt-get install -y php5")

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        self.image_tag = 'codebox/php5'

    def run(self, *args, **kwargs):
        command = ['php5', self.srcname]
        return self.run_cmd(command, *args, **kwargs)
