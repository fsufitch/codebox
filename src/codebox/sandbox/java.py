from codebox.sandbox.sandbox import GenericSandbox

RUNSCRIPT = """
javac {src};
java {compiled};
"""

class Java8Sandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None, client_args={}):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        if not srcname.endswith('.java'):
            raise ValueError("Source name must end in .java: %s" % srcname)

        super(Java8Sandbox, self).__init__(client_args=client_args)
        self.dockerfile[0] = 'FROM dockerfile/java:oracle-java8'

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        runscript_contents = RUNSCRIPT.format(src=srcname,
                                              compiled=srcname[:-5])
        self.include_file("runscript.sh", source_contents=runscript_contents)

        self.image_tag = 'codebox/java8'

    def run(self, *args, **kwargs):
        command = ['sh', 'runscript.sh']
        return self.run_cmd(command, *args, **kwargs)
