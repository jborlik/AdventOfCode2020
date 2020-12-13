#import itertools
#import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time


with open('day13.dat') as datafile:
    allstarttime = int(datafile.readline())
    alldata = datafile.readline().strip().split(',')

teststarttime = 939
testdata = '7,13,x,x,59,x,31,19'.split(',')

thedata = testdata
thestarttime = teststarttime
thedata = alldata
thestarttime = allstarttime

START = time.perf_counter()

lowestbusid = 0
lowestwaittime = 1000000
maxbusid = 0
maxbusidloc = 0
for i, aBus in enumerate(thedata):
    if aBus != 'x':
        iBus = int(aBus)
        diff = thestarttime % iBus
        cycles = int(thestarttime / iBus)
        if diff == 0:
            waittime = 0
        else:
            waittime = (cycles+1) * iBus - thestarttime
        #print(f"Bus {iBus}: {cycles}, nearest {cycles*iBus}, waittime {waittime}")
        if waittime < lowestwaittime:
            lowestwaittime = waittime
            lowestbusid = iBus 
        if iBus > maxbusid:
            maxbusid = iBus
            maxbusidloc = i

print(f"Lowest bus id={lowestbusid} wait time={lowestwaittime} val={lowestbusid*lowestwaittime}")

END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


START = time.perf_counter()

def isValidAroundThisTime(itimemax):
    # now let's check if the buses match up around this time
    for i, aBus in enumerate(thedata):
        if aBus != 'x':
            iBus = int(aBus)
            thistime = itimemax - (maxbusidloc -i)
            diff = thistime % iBus
            if diff != 0:
                return False
    return True
    


icycle = 0
while True:
    icycle += 1
    itimemax = maxbusid * icycle
    gotit = isValidAroundThisTime(itimemax)
    if gotit:
        break

itimestart = icycle*maxbusid - maxbusidloc
print(f"Part 2:  at {itimestart}")

END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")