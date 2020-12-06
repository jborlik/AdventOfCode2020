#import itertools
#import numpy
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])


with open('day06.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """abc

a
b
c

ab
ac

a
a
a
a

b""".splitlines()]

thedata = alldata
#thedata = testdata

countpart1 = 0
countpart2 = 0
currentset = {}
currentgrouptot = 0
for iline, aline in enumerate(thedata):
    if aline == '' or iline==len(thedata)-1:
        if len(aline) > 0:
            # add it in too
            currentgrouptot += 1
            for c in aline:
                currentset[c] = currentset.get(c, 0) + 1
        # end of a group, so process it
        print(f"Group done:  {currentset}")
        # for part 1, just count the number of entries in the set
        countpart1 += len(currentset)

        # for part 2, need to count just the entries where all group members did it
        fullkeys = [k for k,v in currentset.items() if v == currentgrouptot]
        countpart2 += len(fullkeys)

        currentset = {}
        currentgrouptot = 0
    else:
        # this is a person, so add it to the group
        currentgrouptot += 1
        for c in aline:
            currentset[c] = currentset.get(c, 0) + 1


print(f"Part 1: {countpart1}")
print(f"Part 2: {countpart2}")