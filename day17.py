#import itertools
#import numpy as np
import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time

with open('day17.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """.#.
..#
###""".splitlines()]   # 


thedata = testdata
thedata = alldata

#  parse initial state into list of actives
actives = []
rowrange = [0, len(thedata)]
colrange = [0, len(thedata[0])]
zrange = [0,1]
wrange = [0,1]
for irow, aline in enumerate(thedata):
    for icol, achar in enumerate(aline):
        if achar == '#':
            actives.append( (irow, icol, 0, 0) )

neighboroffsets = []
for iw in range(-1,2):
    for irow in range(-1,2):
        for icol in range(-1,2):
            neighboroffsets.append( (irow,icol, 1, iw) )
            neighboroffsets.append( (irow,icol, -1, iw) )
            if not(irow==0 and icol==0 and iw==0):
                neighboroffsets.append( (irow, icol, 0, iw) )

def countNeighbors(t0data, irow, icol, iz, iw):
    count = 0
    for offset in neighboroffsets:
        if (irow+offset[0], icol+offset[1], iz+offset[2], iw+offset[3]) in t0data:
            count += 1
    return count

def makeActive(t1data, irow, icol, iz, iw, rowrange, colrange, zrange, wrange):
    t1data.append( (irow,icol,iz, iw) )
    if irow < rowrange[0]:
        rowrange[0] = irow
    if irow >= rowrange[1]:
        rowrange[1] = irow + 1
    if icol < colrange[0]:
        colrange[0] = icol
    if icol >= colrange[1]:
        colrange[1] = icol + 1
    if iz < zrange[0]:
        zrange[0] = iz
    if iz >= zrange[1]:
        zrange[1] = iz + 1
    if iw < wrange[0]:
        wrange[0] = iw
    if iw >= wrange[1]:
        wrange[1] = iw + 1

def stepInTime(t0data, rowrange, colrange, zrange, wrange):
    newrowrange = [100,-100]
    newcolrange = [100,-100]
    newzrange = [100,-100]
    newwrange = [100,-100]

    t1data = []
    for iw in range(wrange[0]-1,wrange[1]+1):
        for iz in range(zrange[0]-1,zrange[1]+1):
            for irow in range(rowrange[0]-1, rowrange[1]+1):
                for icol in range(colrange[0]-1, colrange[1]+1):
                    iscurrentlyactive = (irow,icol,iz, iw) in t0data
                    count = countNeighbors(t0data,irow,icol,iz,iw)
                    if iscurrentlyactive:
                        if count == 2 or count == 3:
                            makeActive(t1data,irow,icol,iz,iw, newrowrange,newcolrange,newzrange,newwrange)
                        else:
                            pass  # don't add to new list
                    else:
                        if count == 3:
                            makeActive(t1data, irow, icol, iz, iw, newrowrange, newcolrange, newzrange, newwrange )
    return (t1data, newrowrange,newcolrange,newzrange,newwrange)

START = time.perf_counter()


print(f"Before stepping: {rowrange} {colrange} {zrange}:  {actives}")
for istep in range(1,6+1):
    actives, rowrange, colrange, zrange,wrange = stepInTime(actives,rowrange,colrange,zrange,wrange)

    print(f"After step {istep}: {rowrange} {colrange} {zrange}:  {actives}")

print(f"Part 2: count of actives: {len(actives)}")


END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")



START = time.perf_counter()




END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")