#import itertools
#import numpy as np
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time

with open('day14.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".splitlines()]   # 


thedata = testdata
thedata = alldata


START = time.perf_counter()

mem = {}
setmask = 0
clearmask = 0

def createMasks(sMask):
    setmask = 0
    clearmask = 0
    for iChr, aChr in enumerate(sMask[::-1]):
        if aChr=='1':
            setmask = setmask | (1 << iChr)
        elif aChr=='0':
            clearmask = clearmask | (1 << iChr)
    return setmask, clearmask

re_parseMem = re.compile(r'mem\[(\d+)\] = (\d+)')



for aLine in thedata:
    if aLine[0:3] == 'mas':
        # this changes the mask
        setmask,clearmask = createMasks(aLine[len("mask = "):])
    elif aLine[0:3] == 'mem':
        # sets a value
        m = re_parseMem.match(aLine)
        iMem = int(m[1])
        iVal = int(m[2])
        iVal = iVal | setmask
        iVal = iVal & ~(clearmask)
        mem[iMem] = iVal
        #print(f"     Setting {iMem} = {iVal}")

tot = 0
for key, val in mem.items():
    tot += val

print(f"Part 1: sum = {tot}")


END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


START = time.perf_counter()
mem = {}
setmask = 0
floatbits = []

testdata = [x.strip() for x in """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines()]   # 

# thedata = testdata

def setMasksV2(sMask):
    global setmask, floatbits
    setmask = 0
    floatbits = []
    for iChr, aChr in enumerate(sMask[::-1]):
        if aChr=='1':
            setmask = setmask | (1 << iChr)
        elif aChr=='X':
            floatbits.append(iChr)


for aLine in thedata:
    if aLine[0:3] == 'mas':
        # this changes the mask
        setMasksV2(aLine[len("mask = "):])
    elif aLine[0:3] == 'mem':
        # sets a value
        m = re_parseMem.match(aLine)
        iMem = int(m[1])
        iVal = int(m[2])

        iMem = iMem | setmask

        for bits in range(0,2**len(floatbits)):
            onemask = 0
            zeromask = 0
            for iindex, ibit in enumerate(floatbits):
                if (1 << iindex) & bits:
                    onemask = onemask | (1 << ibit)
                else:
                    zeromask = zeromask | (1 << ibit)
            iMem0 = iMem | onemask
            iMem0 = iMem0 & ~zeromask
            print(f"setting {iMem0} = {iVal}")
            mem[iMem0] = iVal


tot = 0
for key, val in mem.items():
    tot += val

print(f"Part 2: sum = {tot}")

END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")