from codebox.sandbox.sandbox import GenericSandbox

RUNSCRIPT = """
/usr/bin/gcc {src} -o runme;
./runme;
"""

class CSandbox(GenericSandbox):
    def __init__(self, srcname, codepath=None, codesource=None):
        if not (codepath or codesource):
            raise ValueError("Must specify code path or code source")
        super(CSandbox, self).__init__()
        self.dockerfile[0] = 'FROM gcc' # Wow.
        self.dockerfile.append("RUN apt-get install -y gcc libc6")

        self.srcname = srcname
        self.include_file(self.srcname, 
                          source_fname=codepath,
                          source_contents=codesource,
                          )

        runscript_contents = RUNSCRIPT.format(src=srcname)
        self.include_file("runscript.sh", source_contents=runscript_contents)

        self.image_tag = 'codebox/c'

    def run(self):
        command = ['sh', 'runscript.sh']
        return self.run_cmd(command)
