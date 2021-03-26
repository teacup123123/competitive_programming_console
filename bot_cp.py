import traceback
from abc import abstractmethod
import urllib.request
import sys
from typing import List
from threading import Thread
import os

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome as ch
from selenium.webdriver import ChromeOptions
import os.path as pth
import time
import re
import os
from selenium.webdriver.chrome.webdriver import WebDriver

_driver: WebDriver = None
solving = 'sol.cpp'
reference = 'sol_0.cpp'
solution_format = 'sol_{}.cpp'
generator = 'input_injection.py'


def get_driver():
    '''get driver, initializes new one if not present'''
    global _driver
    if _driver is None:
        opt = ChromeOptions()
        opt.add_experimental_option("detach", True)
        for addr in [r'C:\Users\user\AppData\Local\Google\Chrome\User Data\Default',
                     r'C:\Users\tchang\AppData\Local\Google\Chrome\User Data\Default']:
            try:
                opt.add_argument(rf"user-data-dir={addr}")
                _driver = webdriver.Chrome(options=opt)
            except Exception as e:
                continue
            break
        try:
            _driver.get('chrome://discards/')
        except Exception:
            raise e
        while '✘️' not in _driver.find_element_by_tag_name('body').text:
            time.sleep(0.5)
            pass
        print('toggled!')
    return _driver


def inject(dst, template, ins, outs, infr, outfr):
    '''inject inputs/outputs into the relevent position( infr, outfr) in template'''
    with open(dst, 'w') as f:
        template.insert(outfr + 1, '\n')
        for o in reversed(outs):
            insertion = f'''\nR"({o})",'''
            template.insert(outfr + 1, insertion)
        template.insert(infr + 1, '\n')
        for i in reversed(ins):
            insertion = f'''\nR"({i})",'''
            template.insert(infr + 1, insertion)
        f.write(''.join(template))


def atcoder_dfs(filename, got, inject_into, treated: set):
    if filename in treated:
        return
    treated.add(filename)
    with open(f'atcoder/{filename}', 'r') as f:
        for readline in reversed(f.readlines()):
            match = re.match('#include "atcoder/([\w_.]+)"', readline)
            if match:
                atcoder_dfs(match.group(1), got, inject_into, treated)
            else:
                got.insert(inject_into, readline)


class bot_cp:
    def __init__(self):
        self.contestname = '_'
        self.prob_codes = []
        self.prob_code = None

    def clr(self):
        '''clears the workspace'''
        files = os.listdir('.')
        avoid = [reference]
        for f in files:
            if f not in avoid and f.endswith('.cpp') and f.startswith('sol'):
                os.remove(f)
        with open(reference, 'r') as f0:
            with open(solving, 'w') as f:
                f.write(f0.read(-1))

    def digest(self):
        with open(solving, 'r') as f:
            got = f.readlines()
            file_format = solution_format.format("(\w+)")
            prob_code, contestname = re.match(f'//{file_format} (\w+)', got[0]).groups()
            prob_codes = re.match("//(([\w+ ]+))", got[1]).groups()[0].split(' ')
        return got, prob_code, contestname, prob_codes

    @abstractmethod
    def prep(self, contestname):
        '''crawls a contest'''
        pass

    @abstractmethod
    def prept(self, prob_code, autoload):
        '''crawls a problem'''
        pass

    def save(self, prob_code):
        '''backs up the problem into x.cpp'''
        pass

    def load(self, prob_code):
        '''loads a particular problem'''

        # old header in solving
        got_, prob_code_, contestname_, prob_codes_ = self.digest()

        if prob_code_.lower() != prob_code.lower() and contestname_ != '_':  # setting _ disactivates backing up
            backupinto = solution_format.format(prob_code_.lower())
            print(f'backing up {solving} into {backupinto}')

            # snapshots input_injection.py into the source code
            fr = got_.index(f'/* {generator}\n') + 1
            to = got_.index(f'{generator} */\n')
            with open(generator, 'r') as f:
                del got_[fr:to]
                for l in reversed(f.readlines()):
                    got_.insert(fr, l)
            with open(backupinto, 'w') as f:
                f.writelines(got_)

        self.prob_code = prob_code
        with open(solution_format.format(prob_code.lower()), 'r') as f:
            got_ = f.readlines()

        fr = got_.index('//<manual-imports-src>\n') + 1
        to = got_.index('//</manual-imports-src>\n')
        for i in range(fr, to):
            if got_[i].startswith('//'):
                got_[i] = got_[i][2:]

        fr = got_.index('//<python-autoimport-src>\n') + 1
        to = got_.index('//</python-autoimport-src>\n')
        del got_[fr:to]

        fr = got_.index(f'/* {generator}\n') + 1
        to = got_.index(f'{generator} */\n')
        dir, _ = os.path.split(__file__)
        with open(os.path.join(dir, generator), 'w') as f:
            f.writelines(got_[fr:to])
        with open(solving, 'w') as f:
            f.writelines(got_)
        print(f'problem {prob_code} loaded {solution_format.format(prob_code)}')

    @abstractmethod
    def sub(self):
        '''submits or copies to clipboard the current cf.cpp'''
        pass

    def incl(self):
        '''expands the include headers into real code'''
        with open(solving, 'r') as f:
            got: List = f.readlines()
            for scanfrom in range(len(got)):
                if got[scanfrom].startswith("//<manual-imports-src>"): break
            for scanto in range(len(got)):
                if got[scanto].startswith("//</manual-imports-src>"): break
            for inject_from in range(len(got)):
                if got[inject_from].startswith("//<python-autoimport-src>"): break
            for inject_into in range(len(got)):
                if got[inject_into].startswith("//</python-autoimport-src>"): break
            del got[inject_from + 1:inject_into]
            inject_into = inject_from + 1
            for li in range(scanfrom + 1, scanto):
                line = got[li]
                matched = re.match('[/]*#include "libs/(\S+)\.h"', line)
                if matched:
                    print(f'\t{line[:-1] if not line.startswith("//") else line[2:-1]}')
                    filename, *_ = matched.groups()
                    if not line.startswith('//'):
                        got[li] = '//' + line
                    with open(f'libs/{filename}.h', 'r') as f:
                        for readline in reversed(f.readlines()):
                            got.insert(inject_into, readline)
                else:
                    matched = re.match('[/]*#include "atcoder/([\S.]+)"', line)
                    if matched:
                        print(f'\t{line[:-1] if not line.startswith("//") else line[2:-1]}')
                        filename, *_ = matched.groups()
                        if not line.startswith('//'):
                            got[li] = '//' + line

                        atcoder_dfs(filename, got, inject_into, set())
        pyperclip.copy(''.join(got))
        # with open(solving, 'w') as f:
        #     f.writelines(got)

    def cp(self):
        '''copies code to clipboard'''
        with open(solving, 'r') as f:
            got = f.readlines()
            full = ''.join(got)
        pyperclip.copy(full)

    def add(self, lib_name):
        if lib_name:
            with open(f'libs/{lib_name}.h', 'r') as f:
                cp_src: List = f.readlines()
                fr, to = None, None
                for _, l in enumerate(cp_src):
                    if l.startswith('#define'):
                        fr = _
                    if l.startswith('#endif'):
                        to = _
                cp_src = cp_src[to - 1:fr:-1]
            with open(solving, 'r') as f:
                got: List = f.readlines()
                into = 0
                for _, l in enumerate(got):
                    if '//<python-copy-here>' in l:
                        into = _
                        break
                for l in cp_src:
                    got.insert(into, l)
            with open(solving, 'w') as f:
                f.writelines(got)


def interface(c=bot_cp()):
    while True:
        try:
            sentence = input()
            function, *parameters = sentence.split()
            if function == 'boot':
                get_driver()
            elif function == 'break':
                _driver.close()
                break
            else:
                getattr(c, function)(*parameters)
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    interface()
