import os
from datetime import datetime

from project_root import *

__par_cpp_dir__ = proot('..')

authors = 'tpyj'
author = 'x'
input_code = 'x'


def setAuthor(name):
    assert name in authors
    global author
    author = name


def setInput(name):
    global input_code
    input_code = name
