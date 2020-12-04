#import itertools
#import numpy
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])

re_p = re.compile(r'(\d+)-(\d+) (\w): (\w+)')

def parsePassword(aLine):
    """Returns a structure (minL, maxL, letter, password)"""
#    print(aLine)
    m = re_p.match(aLine)
#    print(m[1], m[2], m[3])
    if m:
        return (int(m[1]), int(m[2]), m[3], m[4])
    return None

def testIsValid(aPassword):
    num = aPassword[3].count(aPassword[2])
    if (num >= aPassword[0]) and (num <= aPassword[1]):
        return 1
    else:
        return 0

def testIsValidPart2(aPassword):
    c1 = (aPassword[3][aPassword[0]-1] == aPassword[2])
    c2 = (aPassword[3][aPassword[1]-1] == aPassword[2])
    if c1 + c2 == 1:
        return 1
    else:
        return 0

with open('day02.dat') as datafile:
    alldata = [parsePassword(x) for x in datafile.readlines()]

testdata_arr = ['1-3 a: abcde',
'1-3 b: cdefg',
'2-9 c: ccccccccc']    # should result in 2 correct
testdata = [parsePassword(x) for x in testdata_arr]

count = 0
for aP in alldata:
    count += testIsValid(aP)

print(f"Part 1: {count}")

count = 0
for aP in alldata:
    count += testIsValidPart2(aP)

print(f"Part 2: {count}")
