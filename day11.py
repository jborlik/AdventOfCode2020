#import itertools
#import numpy as np
import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
import time


with open('day11.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()]

thedata = testdata
thedata = alldata

START = time.perf_counter()

ROWS = len(thedata)
COLS = len(thedata[0])

OPEN = 'L'
FILL = '#'

def extendIndexToSeat(data, row, col, rowDir, colDir):
    arow = row + rowDir
    acol = col + colDir
    if arow < 0 or arow >= ROWS or acol < 0 or acol >= COLS:
        return arow, acol   # this will be picked up by countNeighbors
    if data[arow][acol] == '.':
        return extendIndexToSeat(data, arow, acol, rowDir, colDir)
    return arow, acol  # this is a seat

def countNeighbors(data, row, col, extendToSeat=False):
    # (-1,-1), (-1,0), (-1,1)
    # (0, -1),       , (0, 1)
    # (1, -1), (1, 0), (1, 1)
    offsets = [ (-1, -1), (-1, 0), (-1,1), (0,-1), (0,1), (1,-1), (1, 0), (1,1)]
    countOpen = 0
    countFilled = 0
    for aOffset in offsets:
        arow = row + aOffset[0]
        acol = col + aOffset[1]
        if extendToSeat:
            arow, acol = extendIndexToSeat(data, row, col, aOffset[0], aOffset[1])

        if arow >= 0 and arow < ROWS and acol >= 0 and acol < COLS:
            countOpen += (1 if data[arow][acol] == OPEN else 0)
            countFilled += (1 if data[arow][acol] == FILL else 0)
    return (countOpen, countFilled)


def nextTimeStep(t0, extendToSeat):
    t1 = copy.deepcopy(t0)
    allowedneighbors = 4
    if extendToSeat:
        allowedneighbors = 5

    for row in range(0,ROWS):
        for col in range(0,COLS):
            _, countFilled = countNeighbors(t0, row, col, extendToSeat)
            if t0[row][col] == OPEN and countFilled == 0:
                # if open and nobody nearby, fill it
                t1[row] = t1[row][:col] + FILL + t1[row][col+1:]
            if t0[row][col] == FILL and countFilled >= allowedneighbors:
                # if filled and too many (4+), empty it
                t1[row] = t1[row][:col] + OPEN + t1[row][col+1:]

    return t1

t0 = thedata
lastCountFilled = 0
for i in range(0,1000):
    t0 = nextTimeStep(t0, extendToSeat=False)
    countFilled = sum(x.count(FILL) for x in t0)
    if countFilled == lastCountFilled:
        break
    lastCountFilled = countFilled

print(t0)


print(f"Part1: occupied sets={lastCountFilled}")
END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


START = time.perf_counter()
t0 = thedata

lastCountFilled = 0
for i in range(0,1000):
    t0 = nextTimeStep(t0, extendToSeat=True)
    countFilled = sum(x.count(FILL) for x in t0)
    if countFilled == lastCountFilled:
        break
    lastCountFilled = countFilled

print(t0)


print(f"Part2: occupied sets={lastCountFilled} (after {i} iter)")

END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")