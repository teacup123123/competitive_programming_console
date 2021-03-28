import os
import os.path as pth
import re
import time
from threading import Thread
import pyperclip as clip
from selenium.webdriver.common.keys import Keys
import requests
from bot_cp import *
from typing import *


class bot_codejam(bot_cp):

    def __init__(self):
        super().__init__()
        self.encoded = {}
        self.check_score: Optional[Thread] = None

    def prept(self, prob_code: str, autoload=False):
        prob_code = prob_code.lower()
        driver = get_driver()
        contestname = self.contestname
        encoded = self.encoded[prob_code]
        driver.get(f'https://codingcompetitions.withgoogle.com/codejam/round/{contestname}/{encoded}')

        with open(reference, 'r') as f:
            samplecpp: list = f.readlines()
        filename = solution_format.format(prob_code)
        samplecpp[0] = f'//{filename} {contestname}\n'
        samplecpp[1] = f'//{" ".join(self.prob_codes)}\n'

        sample = driver.find_elements_by_class_name('sampleio-wrapper')
        if len(sample) == 0:
            print(f'\tinteractive problem {prob_code} detected!')
            ir = driver.find_element_by_partial_link_text('interactive runner')
            ir = ir.get_attribute('href')
            print('\tdownloading interactive_runner.py')
            ir = requests.get(ir)
            with open('interactive_runner.py', 'wb') as f:
                f.write(ir.content)
            ltt = driver.find_element_by_partial_link_text('testing tool')
            ltt = ltt.get_attribute('href')
            print('\tdownloading local_testing_tool.py')
            ltt = requests.get(ltt)
            with open('local_testing_tool.py', 'wb') as f:
                content = ltt.content
                content = content.replace(b'main()\n', b'''
      from attach_now import attachnow
    
      attachnow(main)''')
                f.write(content)
            for i in range(len(samplecpp)):
                samplecpp[i] = samplecpp[i].replace(
                    '//#define INTERACTIVE 1//interactive',
                    '#define INTERACTIVE 1//interactive'
                )
            with open(filename, 'w') as f:
                f.write(''.join(samplecpp))
        else:
            for i in range(len(samplecpp)):
                if '//Google Code jam outputs' in samplecpp[i]:
                    samplecpp[i] = samplecpp[i][2:]
            srcfr, srcto = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-src>\n')]
            del samplecpp[srcfr + 1:srcto]
            infr, into = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-in>\n')]
            del samplecpp[infr + 1:into]
            outfr, outto = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-out>\n')]
            del samplecpp[outfr + 1:outto]

            sample = sample[0]
            rows = sample.find_elements_by_tag_name('pre')
            ins, outs = [], []
            for r in rows:
                id = r.get_attribute('id')
                if 'input' in id:
                    ins.append(r.text.strip() + '\n')
                if 'output' in id:
                    outs.append(r.text.strip() + '\n')
            with open(filename, 'w') as f:
                samplecpp.insert(outfr + 1, '\n')
                for o in reversed(outs):
                    insertion = f'''R"({o}\n)",'''
                    samplecpp.insert(outfr + 1, insertion)

                samplecpp.insert(infr + 1, '\n')
                for i in reversed(ins):
                    insertion = f'''R"({i}\n)",'''
                    samplecpp.insert(infr + 1, insertion)
                f.write(''.join(samplecpp))
        # now preparing the solution
        print(f'task {prob_code} prepared')
        driver.back()

        if autoload:
            self.load(prob_code)

    def sub(self):
        # self.cp()
        self.incl()
        got, prob_code, contestname, prob_codes = self.digest()
        prob_code = self.prob_code
        driver = get_driver()
        self.submissions[prob_code] += 1

        def report():
            try:
                while self.check_score != None:
                    dst = f'https://codingcompetitions.withgoogle.com/codejam/submissions/{self.contestname}/dGVhY3VwMTIzMTIz'
                    if driver.current_url != dst:
                        driver.get(dst)
                    rows = driver.find_elements_by_class_name('ranking-table__row')
                    rows = rows[1:]
                    latest = '?'
                    foundat = 0
                    for sub_depth, r in enumerate(rows):
                        cells = r.find_elements_by_xpath("./*")
                        for i, c in enumerate(cells):
                            if c.text and self.prob_codes[i] == prob_code:
                                tokens = c.text.split('\n')
                                verdicts = [t for t in tokens if
                                            any(pattern in t for pattern in ['check', 'TLE', 'RE', 'CE', 'WA'])]
                                foundat = sub_depth + 1
                                latest = f'{foundat}-st@{tokens[0]}({"|".join(verdicts)})'
                            if foundat == self.submissions[prob_code]: break
                        if foundat == self.submissions[prob_code]: break
                    print(f'\r{latest}', end='')

                    if latest != '?' and foundat == self.submissions[prob_code]:
                        self.check_score = None
                    time.sleep(2)
            except Exception as e:
                print(traceback.format_exc())

        # self.check_score = Thread(target=report)
        # self.check_score.start()

        if self.prob_codes[-1] != prob_code:
            try:
                self.load(self.prob_codes[self.prob_codes.index(prob_code) + 1])
            except Exception as e:
                print(f'unable to autoload next, either no more next or problem_code not defined:{e}')

        # self.check_score.join()

    def prep(self, contestname):
        driver = get_driver()
        driver.maximize_window()
        self.clr()
        self.contestname = contestname

        driver.get(f'https://codingcompetitions.withgoogle.com/codejam/round/{contestname}/')
        buttons = driver.find_elements_by_class_name('problems-nav-problem-btn')
        for problink in buttons:
            problink.send_keys(Keys.CONTROL + Keys.ENTER)

        links = driver.find_elements_by_class_name('problems-nav-problem-link')
        links = [l.get_attribute('href').split('/')[-1] for l in links]
        self.prob_codes = 'a b c d e f g h i j'.split()[:len(links)]
        self.submissions = {p: 0 for p in self.prob_codes}

        for i, (c, l) in enumerate(zip(self.prob_codes, links)):
            self.encoded[c] = l
            self.prept(c, i == 0)
            loadfirst = False
        driver.get(f'https://codingcompetitions.withgoogle.com/codejam/submissions/{self.contestname}/dGVhY3VwMTIzMTIz')

    def kill(self):
        self.check_score = None


if __name__ == '__main__':
    interface(bot_codejam())
