#import itertools
import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
import collections
import time


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

#thedata = testdata
thedata = alldata

endjolt = np.max(thedata) + 3
thedata = np.append(thedata, [0, endjolt])

thedata = np.sort(thedata)

thedatamin1 = np.diff(thedata)
print(thedatamin1)
ones = np.count_nonzero(thedatamin1 == 1)
threes = np.count_nonzero(thedatamin1 == 3)
print(f"Part 1: Ones={ones} threes={threes}.  1*3 = {ones*threes}")

START = time.perf_counter()

# approach from:  https://github.com/neelakantankk/Advent_of_Code_2020/blob/main/Day_10/day_10.py
# graph of reachable adapters
graph = {}
for jolt in thedata:
    diffs = [(jolt+x) for x in (1,2,3)]
    diffs = [y for y in thedata if y in diffs]
    graph[jolt] = diffs

solution = {0:1}  # number of ways to get to item named by key
for key, value in graph.items():
    if value == []:
        break   #nothing reachable, probably last item
    for val in value:
        if val in solution.keys():
            solution[val] += solution[key]   # add all of the ways to get here, to the target
        else:
            solution[val] = solution[key]

END = time.perf_counter()

print(f"Part 2: {solution[thedata[-1]]}")
print(f"Time taken for part 2: {END - START} seconds")
