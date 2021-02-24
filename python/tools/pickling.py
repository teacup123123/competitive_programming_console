import re
import os
import tools.naming_files_folders as naming
from project_root import *
import pickle as pk
import numpy as np
import pandas as pd
from tools.parsetxt import __try_load_cpp

author_2_pickle_loc = {
    x: proot(x, 'pickles_txt') for x in naming.authors
}
author_2_workspace_loc = {
    x: proot(x, 'pickles_txt', 'shared_vars') for x in naming.authors
}


def contents(variable):
    if isinstance(variable, list) or isinstance(variable, set):
        return ' '.join([f"{len(variable)}"] + [f'{x}' for x in variable])
    elif isinstance(variable, dict):
        variable: dict
        total = [f'{len(variable)}']
        for k, v in variable.items():
            total.append(f'{contents(k)} {contents(v)}')
        return ' '.join(total)
    elif isinstance(variable, tuple):
        return ' '.join(contents(x) for x in variable)
    elif isinstance(variable, np.ndarray):
        return contents(variable.tolist())
    elif isinstance(variable, pd.DataFrame):
        return contents(variable.to_dict("list"))
    else:
        # primitive types
        assert type(variable) != str or ' ' not in variable
        return f'{variable}'


def cpp_signature(variable):
    if isinstance(variable, list):
        return f'vector<{cpp_signature(variable[0])}>'
    if isinstance(variable, set):
        return f'set<{cpp_signature(variable[0])}>'
    elif isinstance(variable, dict):
        variable: dict
        for k, v in variable.items():
            break
        return f'map<{cpp_signature(k)},{cpp_signature(v)}>'
    elif isinstance(variable, tuple):
        return f"tuple<{','.join(cpp_signature(x) for x in variable)}>"
    elif isinstance(variable, np.ndarray):
        return cpp_signature(variable.tolist())
    elif isinstance(variable, pd.DataFrame):
        return cpp_signature(variable.to_dict("list"))
    else:
        # primitive types
        if type(variable) == str: return 'string'
        if type(variable) == int: return 'int'
        if type(variable) == float: return 'float'
        if type(variable) == bool: return 'bool'


def update():
    """
    In short, makes sure that all variables are seen by other users across languages: python and cpp alike

        goes over the cpptxt files and generates .pickle/.txt files alongside those preexisting. Then, from all
         .txt/.pickle files automatically writes .h file that parses the .txt files for cpp to see."""
    dir = author_2_pickle_loc[naming.author]
    py_script = author_2_workspace_loc[naming.author]

    # from cpp
    cppvars = [
        file.replace(".cpptxt", "") for file in os.listdir(dir)
        if file.endswith('.cpptxt')
    ]
    for cppvar in cppvars:
        x = __try_load_cpp(dir, cppvar.replace('.cpptxt', ''))
        dump(x, cppvar.replace('.cpptxt', ''), autoupdate=False, raw_name=True)

    variables = [file for file in os.listdir(dir) if file.endswith('.pickle')]
    variables = [
        re.match('([\w_]+).pickle', file).group(1) for file in variables
    ]

    content = r'''# this file is automatically generated
import pickle as pk
import os
from tools.parsetxt import __try_load_cpp
from project_root import *

__dir, _ = os.path.split(__file__)


def __try_load(var: str):
    try:
        with open(pjoin(__dir, f"{var}.pickle"), "rb") as f:
            return pk.load(f)
    except Exception:
        return None


'''
    with open(py_script, 'w') as file:
        file.write(content)
        file.writelines(f'\n{v} = __try_load("{v}")' for v in variables)
        file.writelines(f'\n{v} = __try_load_cpp(__dir,"{v}")'
                        for v in cppvars)
    distribute = {}
    for v in variables:
        if v[-1] not in distribute:
            distribute[v[-1]] = []
        distribute[v[-1]].append(f'{v[:-2]} = __try_load("{v}")')

    for v in cppvars:
        if v[-1] not in distribute:
            distribute[v[-1]] = []
        distribute[v[-1]].append(f'{v[:-2]} = __try_load_cpp(__dir,"{v}")')

    for k, v in distribute.items():
        if not os.path.exists(proot(naming.author, f'{k}.py')):
            continue
        with open(proot(naming.author, f'{k}.py'), 'w') as f:
            f.write(r'''from tools.parsetxt import __try_load_cpp
from .pickles_txt.shared_vars import __try_load
''')
            f.write('\n'.join(v))

    with open(pjoin(dir, "all.h"), 'r') as file:
        contents: list = file.readlines()
        for i, l in enumerate(contents):
            if 'inject here' in l: start = i + 1
            if 'stop here' in l: stop = i
        del contents[start:stop]
        for v in variables:
            contents.insert(start, f'#include "{v}.h"\n')

    with open(pjoin(dir, "all.h"), 'w') as file:
        file.write(''.join(contents))


def hloc(filename):
    return pjoin(author_2_pickle_loc[naming.author], filename + '.h')


def dump(variable, saveas, autoupdate=True, raw_name=False):
    # for python users
    filename = f'{saveas}.pickle' if raw_name else f'{saveas}_{naming.input_code}.pickle'
    with open(pjoin(author_2_pickle_loc[naming.author], filename),
              'wb') as file:
        pk.dump(variable, file)

    # for cpp users
    txtloc = pjoin(author_2_pickle_loc[naming.author],
                   filename + '.txt')
    with open(txtloc, 'w') as file:
        file.write(contents(variable))

    with open(hloc(filename.replace('.pickle', '')), 'w') as file:
        file.write(r'''
//
// generated automatically
//

#ifndef COMPETETIONS_FILENAME_H
#define COMPETETIONS_FILENAME_H

#include <iostream>
#include <fstream>

#include "..\..\tools\parsetxt.h"

namespace pyauthor {
    type filename() {
        ifstream f(R"(txtloc)");
        type res;
        parsetxt(f, res);
        f.close();
        return res;
    }

}


#endif //COMPETETIONS_FILENAME_H
'''.replace('filename',
            filename.replace('.pickle', '').lower()).replace(
            'FILENAME',
            filename.replace('.pickle', '').upper()).replace(
            'author', naming.author).replace(
            'type', cpp_signature(variable)).replace(
            'txtloc',
            naming.relpath(txtloc,
                           reference=naming.__par_cpp_dir__)))

    if autoupdate: update()


if __name__ == '__main__':
    naming.setAuthor('t')
    update()

    # below is example usage
    # naming.setAuthor('t')
    # naming.setInput('a')
    # pickle(['hello', 'world'], 'list_o_words')
    # pickle({1: (1, 2), 2: (3, 4)}, 'dict_o_tp2')
