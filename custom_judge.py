import random as rd
import time
from attach_now import *

import numpy.random as nrd
import numpy as np
attachnow(lambda: None)

if __name__ == '__main__':
    n = 100
    a = nrd.permutation(n)
    imx = np.argmax(a)
    print(n)
    calls = 0
    while calls < 20:
        tp, *content = input().split()
        if tp == '?':
            calls += 1
            l, r = map(int, content)
            l -= 1
            imx1 = np.argmax(a[l:r])
            backup = a[imx1]
            a[imx1] = -1
            print(np.argmax(a[l:r]))
            a[imx1] = backup

        if tp == '!': assert (int(content[0]) - 1 == imx)
