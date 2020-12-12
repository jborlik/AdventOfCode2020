#import itertools
#import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time


with open('day12.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """F10
N3
F7
R90
F11""".splitlines()]   # results in manhattan dist=25 for part 1

thedata = testdata
thedata = alldata

START = time.perf_counter()

DIRS = [ (1,0),(0,1),(-1,0),(0,-1)]  # north, east, south, west.
DIRNAME = ['n','e','s','w']
ROTNUM = {90:1, 180:2, 270:3, 360:0}

#initial state
dir = 1
loc = [0,0]  # north, east
for instruction in thedata:
    ins = instruction[0]
    arg = int(instruction[1:])
    if ins=='N':
        loc[0] += arg
    elif ins=='E':
        loc[1] += arg
    elif ins=='S':
        loc[0] -= arg
    elif ins=='W':
        loc[1] -= arg
    elif ins=='L':
        rot = ROTNUM[arg]
        dir = (4 + dir - rot) % 4
    elif ins=='R':
        rot = ROTNUM[arg]
        dir = (4 + dir + rot) % 4
    elif ins=='F':
        loc[0] += DIRS[dir][0] * arg
        loc[1] += DIRS[dir][1] * arg
    #print(f"Post ins={instruction},\t Loc = {loc}, dir={DIRNAME[dir]}")


print(f"Part 1:  distance={abs(loc[0]) + abs(loc[1])}")
END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


START = time.perf_counter()

shiploc = [0,0]
wayloc = [1,10]

for instruction in thedata:
    ins = instruction[0]
    arg = int(instruction[1:])
    if ins=='N':
        wayloc[0] += arg
    elif ins=='E':
        wayloc[1] += arg
    elif ins=='S':
        wayloc[0] -= arg
    elif ins=='W':
        wayloc[1] -= arg
    elif ins=='L':
        rot = ROTNUM[arg]
        for _ in range(rot):
            t0 = wayloc[1]
            t1 = -wayloc[0]
            wayloc[0] = t0
            wayloc[1] = t1
    elif ins=='R':
        rot = ROTNUM[arg]
        for _ in range(rot):
            t0 = -wayloc[1]
            t1 = wayloc[0]
            wayloc[0] = t0
            wayloc[1] = t1
    elif ins=='F':
        shiploc[0] += wayloc[0] * arg
        shiploc[1] += wayloc[1] * arg    
    print(f"Post ins={instruction},\t Loc = {shiploc}, wayloc={wayloc}")


print(f"Part 2:  distance={abs(shiploc[0]) + abs(shiploc[1])}")

END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")