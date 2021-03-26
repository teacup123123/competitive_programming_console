import pyautogui as pg
import pyperclip as pc
import time
# from local_testing_tool import IO
#
# io = IO()
#
#
# def res(type=int):
#     return map(type, io.ReadInput())
#
#
# def re(type=int):
#     return int(io.ReadInput())
#
#
# def print(x):
#     io.PrintOutput(f'{x}')


def attachnow(target):
    pg.hotkey('ctrl', 'alt', 'f5')  # auto invoques the attach to dialogue on PH
    pg.hotkey('ctrl', 'alt', 'w')  # auto invoques the attach to dialogue on asus
    time.sleep(1)
    pg.write('solution')
    time.sleep(0.2)
    pg.press('enter')
    time.sleep(1)
    with open('sol.cpp', 'r') as f:
        pc.copy(f.read(-1))
    target()  # please choose pg
