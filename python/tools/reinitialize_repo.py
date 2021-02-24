from project_root import *
import os
from .naming_files_folders import authors


def initialize_repo():
    problist = [x[0] for x in os.listdir(inputs_dir) if x.endswith('.in')] + ['x']
    for user in authors:

        # cleaning all variables
        _dir = proot(user, 'pickles_txt')
        for x in os.listdir(_dir):
            if x not in ['all.h', 'shared_vars.py'] and not os.path.isdir(pjoin(_dir, x)):
                os.remove(pjoin(_dir, x))

        # create a blank .py file for each problem to easily import variables for a problem
        for x in problist:
            with open(proot(user, f'{x}.py'), 'w') as f:
                pass
