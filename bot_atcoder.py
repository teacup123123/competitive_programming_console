import os
import os.path as pth
import re
import time
from threading import Thread
import pyperclip as clip
from selenium.webdriver.common.keys import Keys

from bot_cp import *


class bot_atcoder(bot_cp):

    def prept(self, prob_code: str, autoload=False):
        prob_code = prob_code.lower()
        driver = get_driver()
        contestname = self.contestname
        driver.get(rf'https://atcoder.jp/contests/{contestname}/tasks/{contestname}_{prob_code.lower()}')
        caught = []
        seen = set()
        for cp in driver.find_elements_by_class_name('btn-copy'):
            id = cp.get_attribute('data-target')
            if id not in seen:
                seen.add(id)
                pre = driver.find_element_by_id(id)
                if pre.text:
                    caught.append(pre.text)

        with open(reference, 'r') as f:
            samplecpp: list = f.readlines()
            for idx in range(len(samplecpp)):
                if samplecpp[idx].startswith('        re(T);'):
                    samplecpp[idx] = '//' + samplecpp[idx]  # most likely no T cases in ATCODER
                    break
            srcfr, srcto = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-src>\n')]
            del samplecpp[srcfr + 1:srcto]
            infr, into = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-in>\n')]
            del samplecpp[infr + 1:into]
            outfr, outto = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-out>\n')]
            del samplecpp[outfr + 1:outto]
        #
        ins, outs = caught[0::2], caught[1::2]
        filename = solution_format.format(prob_code)
        samplecpp[0] = f'//{filename} {contestname}\n'
        inject(filename, samplecpp, ins, outs, infr, outfr)

        # now preparing the solution
        print(f'task {prob_code} prepared')
        driver.back()

        if autoload:
            self.load(prob_code)

    def sub(self):
        driver = get_driver()
        with open(solving, 'r') as f:
            got = f.readlines()
            _ = solution_format.format(r'(\w+)')
            task_code, self.contestname = re.match(fr'//{_} (\w+)', got[0]).groups()
            task_code = task_code.lower()
            self.prob_codes, *_ = re.match("//([\w+ ]+)", got[1]).groups()
            self.prob_codes = self.prob_codes.split()

        while driver.current_url != fr'https://atcoder.jp/contests/{self.contestname}/submit':
            driver.get(fr'https://atcoder.jp/contests/{self.contestname}/submit')

        for s in driver.find_elements_by_class_name('select2-selection--single'):
            if s.get_attribute('aria-labelledby') != 'select2-select-task-container':
                continue
            else:
                s.send_keys(' ')
                selection_type = driver.find_element_by_class_name('select2-search__field')
                selection_type.send_keys(task_code + ' -')
                selection_type.send_keys(Keys.ENTER)
                break
        filtered = [s for s in driver.find_elements_by_class_name('select2-selection') if
                    s.get_attribute('role') == 'combobox' \
                    and s.get_attribute('tabindex') == '0' \
                    and s.find_elements_by_class_name('select2-selection__arrow')]
        ffilt = []
        for s in filtered:
            try:
                s.click()
                s.click()
                ffilt.append(s)
            except Exception as e:
                continue
        ffilt[1].click()

        selection_type = driver.find_element_by_class_name('select2-search__field')
        selection_type.send_keys('c++')
        selection_type.send_keys(Keys.ENTER)

        simple_editor = driver.find_element_by_class_name('btn-toggle-editor')
        while simple_editor.get_attribute('aria-pressed') != 'true':
            simple_editor.click()

        src = driver.find_element_by_name('sourceCode')
        self.cp()
        src.send_keys(Keys.CONTROL + 'v')

        driver.find_element_by_id('submit').send_keys(Keys.ENTER)
        lastsubmission = driver.find_elements_by_tag_name('tr')[1]

        def report():
            try:
                while not any(stat in lastsubmission.text for stat in ['AC', 'RE', 'TLE', 'MLE', 'OLE', 'IE', 'WA']):
                    print(f'\r{"|".join(lastsubmission.text.split()[2:])}', end='\r')
                    time.sleep(0.3)
                print(lastsubmission.text)
                driver.get(fr'https://atcoder.jp/contests/{self.contestname}/submit')
                print('report thread died nauturally')
            except Exception:
                print('report thread died unnauturally')


        self.check_score = Thread(target=report)
        self.check_score.start()

        if self.prob_codes[-1] != task_code:
            try:
                self.load(self.prob_codes[self.prob_codes.index(task_code) + 1])
            except Exception as e:
                print(f'unable to autoload next, either no more next or problem_code not defined:{e}')

        self.check_score.join()


    def prep(self, contestname):
        driver = get_driver()
        self.clr()
        self.contestname = contestname = str(contestname)
        driver.get(f'https://atcoder.jp/contests/{contestname}/tasks/')
        problems = driver.find_elements_by_tag_name('tr')[1:]
        problems = [tr.find_element_by_tag_name('td').find_element_by_tag_name('a') for tr in problems]
        self.prob_codes = [x.text for x in problems]
        for problink in problems:
            problink.send_keys(Keys.CONTROL + Keys.ENTER)

        for i, c in enumerate(self.prob_codes):
            self.prept(c, i == 0)

        while driver.current_url != fr'https://atcoder.jp/contests/{contestname}/submit':
            driver.get(fr'https://atcoder.jp/contests/{contestname}/submit')


if __name__ == '__main__':
    interface(bot_atcoder())
