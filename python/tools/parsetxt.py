import os
from project_root import *


def parse(content, ptr=0, ptrend=-1):
    if ptrend == -1:
        ptrend = len(content) - 1

    tp = chr(content[ptr])
    if tp == 'i':
        return int(content[ptr + 2:ptrend])
    elif tp == 'f':
        return float(content[ptr + 2:ptrend])
    elif tp == 's':
        return ''.join(chr(x) for x in content[ptr + 2:ptrend])
    else:
        starts = []
        depth = 0
        while ptr != ptrend + 1:
            olddepth = depth
            c = chr(content[ptr])
            if c == '(': depth += 1
            if c == ')': depth -= 1
            ptr += 1
            if depth == 1 and olddepth != 1:
                starts.append(ptr)
        temp = [
            parse(content, starts[i], starts[i + 1] - 1)
            for i in range(0,
                           len(starts) - 1)
        ]
        if tp == 'L':
            return temp
        elif tp == 'T':
            return tuple(temp)
        elif tp == 'S':
            return set(temp)
        elif tp == 'M':
            return dict(temp)


def __try_load_cpp(__dir, var: str):
    try:
        with open(pjoin(__dir, f"{var}.cpptxt"), "rb") as f:
            return parse(f.read(-1))
    except Exception:
        return None
