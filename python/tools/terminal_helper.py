import traceback
import os
from project_root import *
from shutil import copyfile
from tools.reinitialize_repo import initialize_repo
from tools.pickling import update
import tools.naming_files_folders

import re

main = {x: proot(f'main_{x}.py') for x in tools.naming_files_folders.authors}

template = r'''from tools import *
import t
import y
import p
import j

setAuthor('AUTHORCODE')

if __name__ == '__main__':
    setInput(INPUTCODE) 
    #f = offline_input_reader(naming.input_code)
    pass
'''


class daemon:
    def __init__(self):
        self.USER = 'x'

    def user(self, single_letter):
        """indentify yourself as one of the authors"""
        self.USER = single_letter
        assert single_letter in tools.naming.authors

    def new(self, x="'x'", autobackup=True):
        '''backs up the old[if present] main_x.py and prepares a new one, where x is the user code'''
        if autobackup and os.path.exists(main[self.USER]):
            self.save('auto_backup')
        with open(main[self.USER], 'r') as f:
            found = re.findall('setInput\([\'\w\"]+\)', f.read())
        x = 'x'
        for _ in found:
            x = re.match('setInput\(([\'\w\"]+)\)', _).groups(1)[0]
        with open(main[self.USER], 'w') as f:
            f.write(
                template.replace('AUTHORCODE',
                                 self.USER).replace('INPUTCODE', x))

    def save(self, saveas):
        '''saves the current file into x/archive/'''
        copyfile(main[self.USER], proot(self.USER, 'archives', saveas + '.py'))

    def saven(self, saveas):
        '''saves (into the archive) and create a new script'''
        self.save(saveas)
        self.new(autobackup=False)

    def load(self, loadfrom='auto_backup'):
        '''backup main and load from the archive.'''
        if loadfrom + '.py' != 'auto_backup.py':
            self.save('auto_backup')
        src = proot(self.USER, 'archives', loadfrom + '.py')
        dst = main[self.USER]
        print(f'{src}\n >> \n{dst}')
        copyfile(src, dst)

    def steal(self, src_user, loadfrom):
        """steal a script from the archives of another user"""
        self.save('auto_backup')
        src = proot(src_user, 'archives', loadfrom + '.py')
        dst = main[self.USER]
        print(f'{src}\n >> \n{dst}')
        copyfile(src, dst)

    def dinp(self):
        """delete all inputs, use with caution"""
        for f in os.listdir(inputs_dir):
            os.remove(proot('inputs', f))

    def ls(self):
        """list all of the functions"""
        all_attrs = dir(self)
        methods = filter(lambda x: x[0] != "_" and callable(getattr(self, x)),
                         all_attrs)
        for method in methods:
            print(method, ":", getattr(self, method).__doc__)
        print()

    def init(self):
        """initialize the repo (for all users). Use with care"""
        initialize_repo()

    def update(self, *all):
        """update one's own variables --or-- 'update all' to update for all users"""
        users = ''
        if all == 'all':
            users = tools.naming.authors
        if tools.naming.author != 'x':
            users += tools.naming.author
        for u in users:
            tools.naming.setAuthor(u)
            update()


def interface(c=daemon()):
    while True:
        try:
            sentence = input()
            function, *parameters = sentence.split()
            if function in 'break x stop close'.split():
                break
            else:
                getattr(c, function)(*parameters)
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    interface()
