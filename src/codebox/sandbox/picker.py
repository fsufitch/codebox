import mimetypes
from codebox.sandbox.c import CSandbox
from codebox.sandbox.java import Java8Sandbox
from codebox.sandbox.pascal import PascalSandbox
from codebox.sandbox.php import PHP5Sandbox
from codebox.sandbox.python import PythonSandbox, LegacyPythonSandbox
from codebox.sandbox.scala import ScalaSandbox

SANDBOXES = {
    'c': CSandbox,
    'java8': Java8Sandbox,
    'legacypython': LegacyPythonSandbox,
    'pascal': PascalSandbox,
    'php5': PHP5Sandbox,
    'python': PythonSandbox,
    'scala': ScalaSandbox,
    }

def pick_sandbox(sbtype):
    if sbtype not in SANDBOXES:
        raise ValueError("Unknown sandbox type: %s" % sbtype)
    return SANDBOXES[sbtype]

def guess_sandbox(fname):
    mime = mimetypes.guess_type(fname)
    if fname.endswith('.php'):
        return 'php5'
    if 'x-python' in mime[0]:
        return 'python'
    if 'x-csrc' in mime[0]:
        return 'c'
    if 'x-java' in mime[0]:
        return 'java8'
    if 'x-scala' in mime[0]:
        return 'scala'
    if 'x-pascal' in mime[0]:
        return 'pascal'
    raise ValueError('Cannot guess sandbox type from filename only: %s' % fname)
