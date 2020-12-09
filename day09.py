import itertools
import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])


with open('day09.dat') as datafile:
    alldata = np.array([int(x.strip()) for x in datafile.readlines()])

testdata = np.array([int(x.strip()) for x in """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".splitlines()])

thedata = testdata
preamble = 5  # part 1: 127
thedata = alldata
preamble = 25

def isIValid(fullarray, i):
    value = fullarray[i]
    for a,b in itertools.permutations(fullarray[i-preamble:i],2):
        if a+b==value:
            return True
    return False

invalidnumber = 0
for i in range(preamble,len(thedata)):
    value = thedata[i]
    if not isIValid(thedata, i):
        print(f"Part 1: Found invalid at {i}:  {thedata[i]}")
        invalidnumber = thedata[i]

# approach for part 2:  brute force.   outer loop=starting index, inner=inc end index until sum == or sum >

for istart in range(0, len(thedata)):
    sum = thedata[istart] + thedata[istart+1]
    iend = istart+2
    while sum < invalidnumber:
        sum += thedata[iend]
        iend += 1
    if sum == invalidnumber:
        print(f"Part 2:  Found sum range from {istart} to {iend}")
        small = np.min(thedata[istart:iend])
        big = np.max(thedata[istart:iend])
        print(f"        Smallest={small} biggest={big} sum={small+big}")
        break



print("done")