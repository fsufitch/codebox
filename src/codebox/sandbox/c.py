from codebox.sandbox.sandbox import GenericSandbox

RUNSCRIPT = """
gcc {src} -o runme;
./runme;
"""

class CSandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None, client_args={}):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        super(CSandbox, self).__init__(client_args=client_args)
        self.dockerfile[0] = 'FROM gcc' # Wow.
        #self.dockerfile.append("RUN apt-get install -y gcc libc6")

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        runscript_contents = RUNSCRIPT.format(src=srcname)
        self.include_file("runscript.sh", source_contents=runscript_contents)

        self.image_tag = 'codebox/c'

    def run(self, *args, **kwargs):
        command = ['sh', 'runscript.sh']
        return self.run_cmd(command, *args, **kwargs)
