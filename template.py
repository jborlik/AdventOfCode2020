#import itertools
#import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time
#import pprint


with open('day17.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""".splitlines()]   # 


thedata = testdata
#thedata = alldata



# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------


START = time.perf_counter()


END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

START = time.perf_counter()




END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")