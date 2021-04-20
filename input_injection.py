import itertools as it
# re() and res() are not defined since this is non-interactive

T_defined = 0
testcases = []

with open('cf.cpp', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if '//<test case>' in line:
            T_defined = not line.startswith('//')
            break


def build_testcase(params):  # TODO change the parameter here
    # TODO generate the content for the format
    testcase = []
    # ------------------------------------------------------
    n = params
    testcase.append(f'''{" ".join(f"{p}" for p in params)}''')
    # testcase.append(f'''more lines to follow''')
    # testcase.append(f'''more lines to follow''')
    # testcase.append(f'''more lines to follow''')

    # ------------------------------------------------------
    return '\n'.join(testcase)


# TODO scan the parameters
for params in it.product(*[[],]):
    testcases.append(build_testcase(params))

if T_defined:
    print(f'\t{len(testcases)}')
    for tc in testcases:
        print(tc)
else:
    for tc in testcases:
        print('\t' + tc)

