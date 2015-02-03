from codebox.sandbox.sandbox import GenericSandbox

RUNSCRIPT = """
fpc {src} > /dev/null;
./{compiled};
"""

class PascalSandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        if not srcname.endswith('.pas'):
            raise ValueError("Source name must end in .pas: %s" % srcname)
        super(PascalSandbox, self).__init__()
        #self.dockerfile[0] = 'FROM gcc' # Wow.
        self.dockerfile.append("RUN apt-get update")
        self.dockerfile.append("RUN apt-get install -y fp-compiler")

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        runscript_contents = RUNSCRIPT.format(src=srcname,
                                              compiled=srcname[:4])
        self.include_file("runscript.sh", source_contents=runscript_contents)

        self.image_tag = 'codebox/pascal'

    def run(self, *args, **kwargs):
        command = ['sh', 'runscript.sh']
        return self.run_cmd(command, *args, **kwargs)
