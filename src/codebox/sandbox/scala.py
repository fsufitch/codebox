from codebox.sandbox.sandbox import GenericSandbox

RUNSCRIPT = """
scalac {src};
scala {compiled};
"""

class ScalaSandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None, client_args={}):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        if not srcname.endswith('.scala'):
            raise ValueError("Source name must end in .scala: %s" % srcname)

        super(ScalaSandbox, self).__init__(client_args=client_args)
        self.dockerfile[0] = 'FROM williamyeh/scala:latest'

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        runscript_contents = RUNSCRIPT.format(src=srcname,
                                              compiled=srcname[:-6])
        self.include_file("runscript.sh", source_contents=runscript_contents)

        self.image_tag = 'codebox/scala'

    def run(self, *args, **kwargs):
        command = ['sh', 'runscript.sh']
        return self.run_cmd(command, *args, **kwargs)
