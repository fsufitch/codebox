import mimetypes
from codebox.sandbox.python import PythonSandbox, LegacyPythonSandbox
from codebox.sandbox.c import CSandbox


SANDBOXES = {
    'python': PythonSandbox,
    'legacypython': LegacyPythonSandbox,
    'c': CSandbox,
    }

def pick_sandbox(sbtype):
    if sbtype not in SANDBOXES:
        raise ValueError("Unknown sandbox type: %s" % sbtype)
    return SANDBOXES[sbtype]

def guess_sandbox(fname):
    mime = mimetypes.guess_type(fname)
    if 'x-python' in mime[0]:
        return 'python'
    if 'x-csrc' in mime[0]:
        return 'c'
    raise ValueError('Cannot guess sandbox type from filename only: %s' % fname)
