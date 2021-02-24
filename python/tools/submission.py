import io
import os
import zipfile
import tools.naming_files_folders as naming_files_folders
from datetime import datetime
from project_root import *
from submissions.submission_root import __file__ as submissiondir
import pyperclip


def zip_src_and_copy_abs_path(abspath=None, ziplabel=None):
    if ziplabel is None: ziplabel = 'submission'
    submission_folder, _ = os.path.split(submissiondir)
    time = datetime.now().strftime("%Hh%Mm")
    if abspath is None:
        abspath = proot( '..')
    with zipfile.ZipFile(f'{submission_folder}/{naming_files_folders.author}_{ziplabel}_{time}.zip', 'w',
                         zipfile.ZIP_DEFLATED) as ziph:
        # ziph is zipfile handle
        for root, dirs, files in os.walk(abspath):
            for file in files:
                if not any(file.endswith(ext) for ext in ['.cpp', '.h', '.py', '.hpp']):
                    continue
                ziph.write(
                    pjoin(root, file),
                    os.path.relpath(pjoin(root, file), abspath)
                )
    pyperclip.copy(os.path.abspath(ziph.filename))


class wrapped(io.TextIOWrapper):
    def pr(self, *moreargs):
        '''prints with a space'''
        pass

    def ps(self, *moreargs):
        '''prints with a line'''
        pass

    pass


class solutionFile:
    def __init__(self, label, autozip=True):
        assert naming_files_folders.input_code != '?'
        self.file: wrapped
        self.filename = \
            f'{naming_files_folders.author}_' \
            f'{label}_' \
            f'{naming_files_folders.input_code}_' \
            f'{datetime.now().strftime("%Hh%Mm")}.solution'
        self.notempty = False
        if autozip:
            zip_src_and_copy_abs_path(ziplabel=f'{label}_{naming_files_folders.input_code}')
        print(f'opening solution to "{self.filename}"')

    def __enter__(self):
        submission_folder, _ = os.path.split(submissiondir)
        self.file = open(f'{submission_folder}\\{self.filename}', 'w')

        def digest(arg):
            if isinstance(arg, list) or isinstance(arg, tuple):
                arg = ' '.join(digest(x) for x in arg)
            return f'{arg}'

        def print_line(*moreargs):
            self.file.write(' ' * self.notempty + ' '.join(digest(x) for x in moreargs) + '\n')
            self.notempty = False

        def print_space(*moreargs):
            self.file.write(' ' * self.notempty + ' '.join(digest(x) for x in moreargs))
            self.notempty = True

        self.file.pr = print_space
        self.file.ps = print_line
        self.file: wrapped
        return self.file

    def __exit__(self, *args):
        self.file.close()
        print(f'closed solution to "{self.filename}"')


if __name__ == '__main__':
    naming_files_folders.setInput('a')
    naming_files_folders.setAuthor('t')

    with solutionFile('some_algo', autozip=True) as f:
        f.ps(1)
        f.ps(1, 2, 24)
        f.pr(1, 2, 24)
        f.ps(1, 1.445, 24)
        f.ps(1, 1.445, 24)
        f.ps(2)
        f.ps([1, 2, 'hello'])
        f.ps(5)
