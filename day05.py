#import itertools
#import numpy
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])


with open('day05.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = 'FBFBBFFRLR'

def getSeat(aID) -> (int, int):
    rowS = aID[0:7]
    colS = aID[7:10]
    rowS = re.sub('F', '0', rowS)
    rowS = re.sub('B', '1', rowS)
    colS = re.sub('R', '1', colS)
    colS = re.sub('L', '0', colS)
    row = int(rowS, 2)
    col = int(colS, 2)
    return (row,col)

print(f"Test should be (44,5) = {getSeat(testdata)}")

maxID = 0
for aID in alldata:
    rc = getSeat(aID)
    thisid = rc[0]*8 + rc[1]
    if thisid > maxID:
        maxID = thisid

print(f"Part 1: Max = {maxID}")


# make all seats
allseats = {}
for irow in range(1,127):
    for icol in range(0,8):
        allseats[(irow,icol)] = irow*8 + icol

# remove from list
for aID in alldata:
    rc = getSeat(aID)
    #print(f"---pop {rc}")
    allseats.pop(rc)

# print remaining
print(allseats)
