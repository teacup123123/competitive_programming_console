# PROBLEM b
import heapq as hq
import sys
from collections import Counter
from itertools import *
import bisect as bs


def solve(ti):
    pass


def main():
    # start coding here...
    t = re()
    for ti in range(t):
        pr(f'Case #{ti + 1}: ')
        solve(ti + 1)


samples = []

samples.append(("""
4
2020
2021
68000
101

""", """
Case #1: 2021
Case #2: 2122
Case #3: 78910
Case #4: 123

"""))
#SAMPLE


def gen_token():
    for line in sys.stdin:
        for word in line.strip().split():
            yield word


__reader = gen_token()
FLUSH = True


def ps(*content):
    line = ' '.join(f'{x}' for x in content)
    sys.stdout.write(line + '\n')
    if FLUSH:
        sys.stdout.flush()


def pr(*content):
    line = ' '.join(f'{x}' for x in content)
    sys.stdout.write(line)
    if FLUSH:
        sys.stdout.flush()


def re(*tp):
    if len(tp) == 0:
        tp = [int]
    if len(tp) == 1:
        tp0 = tp[0]
        if type(tp0) == type:
            return tp0(next(__reader))
        else:
            if type(tp0) == list:
                for i, x in enumerate(tp0):
                    tp0[i] = re(type(x))
    else:
        return [t(next(__reader)) for t in tp]


def digest(sample: str):
    for line in sample.splitlines():
        for word in line.split():
            yield word


if __name__ == '__main__':
    params = sys.argv[1:]
    if len(params):
        for s, so in samples:
            __reader = digest(s)
            main()
            ps()
            pr("""sample out ---VVV---""")
            pr(so)
            ps("""sample out ---^^^---""")

    else:
        main()
