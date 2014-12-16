import argparse, os
from codebox.sandbox.picker import pick_sandbox, guess_sandbox

DESCRIPTION = 'Run code in a docker.io sandboxed environment'

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--sandbox', metavar="SANDBOX", dest='sandbox', default=None, type=str, help="identifier for type of sandbox to use")
    parser.add_argument('source_file', metavar="SOURCEFILE", help="source file to run")
    args = parser.parse_args()

    srcfile = args.source_file
    sbtype = args.sandbox
    if not sbtype:
        sbtype = guess_sandbox(srcfile)
    
    fname = os.path.split(srcfile)[1]

    sb_cls = pick_sandbox(sbtype)
    sandbox = sb_cls(fname, codepath=srcfile)
    sandbox.build()
    result = sandbox.run()
    sandbox.destroy()

    print("Your code:")
    print(open(srcfile).read())
    print("Result:")
    print(result.decode())
