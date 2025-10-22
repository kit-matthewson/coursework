import argparse
from ast import literal_eval as make_tuple
from simple import solve as ssolve
from advanced import solve as asolve

parser = argparse.ArgumentParser()
parser.add_argument("formula", help="input the formula here")
parser.add_argument("--advanced", help="execute advanced solver", action="store_true")
args = parser.parse_args()


def checkformat(cs):
    if cs[0] == "-" or cs[0] == "+":
        return len(cs) == 3 and checkformat(cs[1]) and checkformat(cs[2])
    elif cs[0] == "~":
        return len(cs) == 2 and checkformat(cs[1])
    else:
        return True


cs = make_tuple(args.formula)
if checkformat(cs):
    if args.advanced:
        if asolve(cs):
            print("SAT")
        else:
            print("UNSAT")
    else:
        if ssolve(cs):
            print("SAT")
        else:
            print("UNSAT")
else:
    print("Format error")

# Testcases

# python3 test.py "('+','a',('-','b',('~','a')))"
# Expected: SAT

# python3 test.py "('+',('+','a',('-','a','b')),('b'))"
# Expected: SAT

# python3 test.py "('+',('+',('-','a','b'),('-','a',('-','b','c'))),('~','c'))"
# Expected: SAT

# python3 test.py "('+',('-','x1','x2'),('-',('~','x2'),'x3'))"
# Expected: SAT

# python3 test.py "('+','a',('~','a'))"
# Expected: UNSAT

# python3 test.py "('+','a',('+','b',('-',('~','a'),('~','b'))))"
# Expected: UNSAT
