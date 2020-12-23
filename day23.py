#import itertools
#import numpy as np
import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
import collections
#import math
import time
#import pprint


alldata = '916438275'

testdata = '389125467'  # 


thedata = testdata
thedata = alldata

_cupring = collections.deque([int(x) for x in thedata])
_cupring_p1 = copy.copy(_cupring)
_cupring_p1.rotate(-1)

cupdict = dict(zip(_cupring, _cupring_p1))
current = _cupring[0]

cupdict_original = copy.deepcopy(cupdict)
current_original = current

# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------

def oneMove(cupdict, current):
    # get the next three cups
    poppedcups = [ cupdict[current], 
                   cupdict[cupdict[current]], 
                   cupdict[cupdict[cupdict[current]]]  ]

    # find destination cup
    iDest = current-1
    while iDest <= 0 or iDest in poppedcups:
        iDest -= 1
        if iDest <= 0:
            iDest = len(cupdict)

    # replace three cups clockwise of dest cup
    cupdict[current] = cupdict[poppedcups[2]]   # remove the three
    cupdict[poppedcups[2]] = cupdict[iDest]
    cupdict[iDest] = poppedcups[0]
    
    return cupdict, cupdict[current]


START = time.perf_counter()

for _ in range(100):
    cupdict, current = oneMove(cupdict, current)
    print(cupdict)

def printHead(cupdict, count):
    print("Cups: ", end='')
    iloc = cupdict[1]
    for _ in range(min(len(cupdict), count-1)):
        print(iloc, end='')
        iloc = cupdict[iloc]
    print()

printHead(cupdict, 9)
        




END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")




# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

START = time.perf_counter()

cupdict = copy.deepcopy(cupdict_original)
current = current_original

extras = dict(zip(range(10,1000001), range(11,1000002)))

cupdict.update(extras)
cupdict[1000000] = _cupring[0]
cupdict[_cupring[-1]] = 10

for imove in range(10000000):
    if (imove % 100000) == 0:
        print(imove)
    cupdict, current = oneMove(cupdict, current)

print("Part 2!")


val1 = cupdict[1]
val2 = cupdict[val1]
print(f"Values:  {val1} x {val2} = {val1*val2}")
# test:  934001  x   159792  = 149245887792

END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")