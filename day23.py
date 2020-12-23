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
#thedata = alldata

cupring = collections.deque([int(x) for x in thedata])
cupring_p1 = copy.copy(cupring)
cupring_p1.rotate(-1)

cupdict = dict(zip(cupring, cupring_p1))
current = cupring[0]

cupring_original = copy.deepcopy(cupring)
current_original = current

# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------

def oneMove(cupring):
    iCurrent = cupring[0]
    # remove 3 cups (step 1)
    cupring.rotate(-1)
    poppedcups = [cupring.popleft(), cupring.popleft(), cupring.popleft()]
    cupring.rotate(1)
    # find destination cup
    iDest = iCurrent-1
    while iDest not in cupring:
        iDest -= 1
        if iDest <= 0:
            iDest = len(cupring)+3
    # replace three cups clockwise of dest cup
    # first move to dest
    while cupring[0] != iDest:
        cupring.rotate(-1)
    cupring.rotate(-1)
    cupring.extendleft(reversed(poppedcups))
    cupring.rotate(1)
    # now move back to current cup
    while cupring[0] != iCurrent:
        cupring.rotate(1)
    # and select a current cup immediately clockwise
    cupring.rotate(-1)
    return cupring

def printFromOne(cupring):
    tmp = copy.copy(cupring)
    while tmp[0] != 1:
        tmp.rotate(1)
    tmp.popleft()
    print("".join(map(str,tmp)))



START = time.perf_counter()

for _ in range(100):
    oneMove(cupring)
    print(cupring)

printFromOne(cupring)

END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

START = time.perf_counter()

cupring = copy.deepcopy(cupring_original)

cupring.extend(range(10,1000001))

for imove in range(10000000):
    if (imove % 1000) == 0:
        print(imove)
    oneMove(cupring)

print("Part 2!")

while cupring[0] != 1:
    cupring.rotate(1)

val1 = cupring[1]
val2 = cupring[2]
print(f"Values:  {val1} x {val2} = {val1*val2}")


END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")