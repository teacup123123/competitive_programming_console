import os
import naming_files_folders
from project_root import *

input_dir, _ = os.path.split(inputs_dir)


class offline_input_reader:
    """Reads and caches an input file in bulk, subsequent calls:

        - ``ntoken`` for next token as a string
        - ``re(int,int,float)`` to read 3 variables of type int,int,float
        - ``re()`` to read a simple integer
    """

    def __init__(self, single_letter_code=None):
        '''if no letter specified will load problem x, where x = naming.input_code'''
        if single_letter_code is None:
            assert naming_files_folders.input_code != 'x'
            single_letter_code = naming_files_folders.input_code

        inputs = filter(
            lambda x: x.startswith(single_letter_code) and not x.endswith('.py'
                                                                          ),
            os.listdir(inputs_dir))
        self.filename: str = ''
        for self.filename in inputs:
            break
        print(f'opened "{self.filename}" fully in one go and caching')
        with open(pjoin(inputs_dir, self.filename), 'r') as f:
            self.lines = [l.split() for l in f.readlines()]
        self.lineptr = 0
        self.wordptr = 0

    def readline(self):
        '''read words from the current position up to end of line'''
        currentline = self.lineptr
        nextline = currentline + 1
        tokens = []
        while currentline != nextline:
            tokens.append(self.ntoken())
        return ' '.join(tokens)

    def ntoken(self):
        '''read a word, delimited by spaces'''
        res = self.lines[self.lineptr][self.wordptr]
        self.wordptr += 1
        if self.wordptr == len(self.lines[self.lineptr]):
            self.lineptr += 1
            self.wordptr = 0
        return res

    def re(self, *args):
        '''reads one int --or-- or read multiple variables'''
        if len(args) == 0:
            args = (int,)
        if len(args) == 1:
            return args[0](self.ntoken())
        return tuple(tp(self.ntoken()) for tp in args)
