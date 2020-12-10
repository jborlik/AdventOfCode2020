#import itertools
import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
import collections


with open('day10.dat') as datafile:
    alldata = np.array([int(x.strip()) for x in datafile.readlines()])

testdata = np.array([int(x.strip()) for x in """16
10
15
5
1
11
7
19
6
12
4""".splitlines()])

thedata = testdata
thedata = alldata

endjolt = np.max(thedata) + 3
thedata = np.append(thedata, [0, endjolt])

thedata = np.sort(thedata)

thedatamin1 = np.diff(thedata)
print(thedatamin1)
ones = np.count_nonzero(thedatamin1 == 1)
threes = np.count_nonzero(thedatamin1 == 3)
print(f"Part 1: Ones={ones} threes={threes}.  1*3 = {ones*threes}")

potentials = collections.deque([ (0, [0]) ])
successes = []

def returnIfValid(iloc, offset, currentlist):
    global successes

    if iloc + offset < len(thedata):
        nextval = thedata[iloc + offset]
        if nextval - thedata[iloc] <= 3:
            if nextval == endjolt:
                successes.append(currentlist + [nextval])
                return (False, False)  # no need to do anything else
            else:
                return (nextval, iloc+offset)
    return (False,False)

while potentials:
    (iloc, aPot) = potentials.popleft()

    nextval, inext = returnIfValid(iloc, 1, aPot)
    if nextval:
        potentials.append( (inext, aPot + [nextval]) )

        nextval, inext = returnIfValid(iloc, 2, aPot)
        if nextval:
            potentials.append( (inext, aPot + [nextval]) )

            nextval, inext = returnIfValid(iloc, 3, aPot)
            if nextval:
                potentials.append( (inext, aPot + [nextval]))

print(f"Part 2: Number of successes = {len(successes)}")
