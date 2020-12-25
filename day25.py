#import itertools
#import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time
#import pprint


#with open('day25.dat') as datafile:
#    alldata = [x.strip() for x in datafile.readlines()]
alldata = [ 11562782, 18108497]   # card, door

testdata = [5764801, 17807724 ] # card, door


thedata = testdata
thedata = alldata



# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------

def transform(subjectnumber, loopsize):
    val = 1
    for _ in range(loopsize):
        val *= subjectnumber
        val = val % 20201227
    return val

def findloopsize(subjectnumber, targetvalue):
    val = 1
    for i in range(10000000000000):
        val *= subjectnumber
        val = val % 20201227
        if val == targetvalue:
            return i+1
    return -1


START = time.perf_counter()

card_pub = thedata[0]
card_loop = findloopsize(7, card_pub)
print(f"Card loop size = {card_loop}")

door_pub = thedata[1]
door_loop = findloopsize(7, door_pub)
print(f"Door loop size = {door_loop}")

encryption_key = transform(door_pub, card_loop)
print(f"Encryption key = {encryption_key}")


END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

START = time.perf_counter()




END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")