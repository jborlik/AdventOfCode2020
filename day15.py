#import itertools
#import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time

#with open('day15.dat') as datafile:
#    alldata = [x.strip() for x in datafile.readlines()]
alldata = [14,8,16,0,1,17]

testdata = [0,3,6]   # 


thedata = testdata
thedata = alldata


START = time.perf_counter()

def playGame(startingnumbers, maxturns) -> int:
    """ returns the number spoken on the maxturns round """
    numbers = {}
    turn = 0
    lastspoken = 0
    while turn < maxturns:
        turn += 1
        spoken = 0
        if turn <= len(startingnumbers):
            spoken = startingnumbers[turn-1]
        else:
            spoken =  (turn-1) - numbers.get(lastspoken,turn-1)

        if turn > 1:
            numbers[lastspoken] = turn-1
        lastspoken = spoken
        #print(f"Turn {turn}, number = {lastspoken}")
    return lastspoken

ilast = playGame(thedata, 2020)
print(f"Part 1:  Last number said was {ilast}")

END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


START = time.perf_counter()

ilast = playGame(thedata, 30000000)
print(f"Part 2:  Last number said was {ilast}")

END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")