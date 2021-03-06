import argparse, os
from codebox.sandbox.picker import pick_sandbox, guess_sandbox

DESCRIPTION = 'Run code in a docker.io sandboxed environment'

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--sandbox', metavar="SANDBOX", dest='sandbox', default=None, type=str, help="identifier for type of sandbox to use")
    parser.add_argument('--apiversion', metavar="APIVERSION", dest='apiversion', default=None, type=str, help="API version for docker-py to use when connecting")
    parser.add_argument('-z', '--zipfile', metavar="ZIP", dest='zip', default=None, type=str, help="zipfile to source files from")
    parser.add_argument('source_file', metavar="SOURCEFILE", help="source file to run")
    args = parser.parse_args()

    srcfile = args.source_file
    zipfile = args.zip

    client_args = {}
    if args.apiversion:
        client_args['version'] = args.apiversion

    sbtype = args.sandbox
    if not sbtype:
        sbtype = guess_sandbox(srcfile)
    
    fname = os.path.split(srcfile)[1]

    sb_cls = pick_sandbox(sbtype)
    sandbox = sb_cls(fname, codepath=srcfile, client_args=client_args)
    if zipfile:
        sandbox.include_zip(source_fname=zipfile)
    sandbox.build()
    result = sandbox.run(cleanup=False)

    print("Your code:")
    print(open(srcfile).read())
    print("Result:")
    print(result['logs'].decode())

    print("Contents of foo.out:")
    data = sandbox.get_file(result['container_id'], 'foo.out')
    print(data)

    sandbox.destroy()
