from os.path import join as pjoin
from os.path import split as psplit
from os.path import relpath as __relpath

pyroot, _ = psplit(__file__)


def proot(*args):
    return pjoin(pyroot, *args)


inputs_dir = proot('inputs')


def relpath(abspath, reference=None):
    return __relpath(abspath, start=pyroot if reference is None else reference)
