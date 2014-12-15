import sys
from codebox.sandbox.sandbox import GenericSandbox
from codebox.sandbox.python import PythonSandbox

def main():
    srcfile = sys.argv[1]
    s = PythonSandbox(srcfile)
    s.build()
    result = s.run()
    print(result)
    s.destroy()
