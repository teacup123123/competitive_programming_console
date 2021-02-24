import os
import os.path as pth
import re
import time
from threading import Thread

from selenium.webdriver.common.keys import Keys

from bot_cp import *


class bot_codeforces(bot_cp):

    def prept(self, prob_code: str, autoload=False):
        driver = get_driver()
        contestname = self.contestname
        driver.get(f'https://codeforces.com/contest/{contestname}/problem/{prob_code.upper()}')

        caught = []
        for element in driver.find_elements_by_tag_name('pre'):
            caught.append(element.text)

        with open(reference, 'r') as f:
            samplecpp: list = f.readlines()
            srcfr, srcto = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-src>\n')]
            del samplecpp[srcfr + 1:srcto]
            infr, into = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-in>\n')]
            del samplecpp[infr + 1:into]
            outfr, outto = [idx for idx, line in enumerate(samplecpp) if line.endswith('python-autofill-out>\n')]
            del samplecpp[outfr + 1:outto]
        #
        ins, outs = caught[0::2], caught[1::2]
        file = solution_format.format(prob_code.lower())
        samplecpp[0] = f'//{file} {contestname}\n'
        samplecpp[1] = f'//{" ".join(self.prob_codes)}\n'
        inject(f'{file}', samplecpp, ins, outs, infr, outfr)

        # now preparing the solution
        print(f'task {prob_code} prepared')
        driver.back()

        if autoload:
            self.load(prob_code)

    def sub(self):
        with open(solving, 'r') as f:
            got = f.readlines()
            _ = solution_format.format(r'(\w+)')
            task_code, self.contestname = re.match(fr'//{_} (\w+)', got[0]).groups()
            task_code = task_code.lower()
            self.prob_codes, *_ = re.match("//([\w+ ]+)", got[1]).groups()
            self.prob_codes = self.prob_codes.split()

        driver = get_driver()
        while driver.current_url != fr'https://codeforces.com/contest/{self.contestname}/submit':
            driver.get(fr'https://codeforces.com/contest/{self.contestname}/submit')
        selection = driver.find_element_by_name('submittedProblemIndex')
        # toggle_editor = driver.find_element_by_class_name('toggleEditorCheckboxLabel') # only for codeforce, multi-character
        selection.send_keys(task_code)
        # editor = driver.find_element_by_tag_name('textarea')
        srcfilebrowse_button = driver.find_element_by_name('sourceFile')
        src_file_loc = os.path.abspath(pth.join(os.getcwd(), solving))
        print(f"uploading file {src_file_loc}")
        srcfilebrowse_button.send_keys(src_file_loc)
        submit = driver.find_element_by_class_name('submit')
        while submit.get_attribute('disabled') == 'disabled':
            print('submit button disabled')
        time.sleep(0.5)
        submit.send_keys(Keys.ENTER)

        def report():
            time.sleep(10)
            while True:
                time.sleep(1)
                driver.refresh()
                table = driver.find_element_by_class_name('status-frame-datatable')
                lastsubmission = table.find_elements_by_tag_name('tr')[1]
                columns = lastsubmission.find_elements_by_tag_name('td')
                columns = [c.text for c in columns]
                print(f'\r{"|".join(columns[3:])}', end='\r')
                verdict = columns[5]
                if any(x in verdict for x in ['Happy', 'ccept', 'ceede', 'rror', 'rong', 'assed']):
                    break
            print('finally: ' + lastsubmission.text)
            driver.get(fr'https://codeforces.com/contest/{self.contestname}/submit')

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

        driver.get(f'https://codeforces.com/contest/{contestname}/')
        table = driver.find_element_by_class_name('problems')
        problems = table.find_elements_by_tag_name('tr')[1:]
        problems = [tr.find_element_by_tag_name('td').find_element_by_tag_name('a') for tr in problems]
        self.prob_codes = prob_codes = [x.text.lower() for x in problems]
        for problink in problems:
            problink.send_keys(Keys.CONTROL + Keys.ENTER)

        for c in prob_codes:
            self.prept(c, autoload=problems[0] == c)

        while driver.current_url != fr'https://codeforces.com/contest/{contestname}/submit':
            driver.get(fr'https://codeforces.com/contest/{contestname}/submit')


if __name__ == '__main__':
    interface(bot_codeforces())
