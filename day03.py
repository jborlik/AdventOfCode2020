#import itertools
#import numpy
#import copy
#import re


with open('day03.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [] 

#alldata = testdata

themap = alldata

def countTrees(xinc, yinc, themap):
    xpos = 0
    ypos = 0
    treecount = 0
    XMAX = len(themap[0])
    while ypos < len(themap):
        if themap[ypos][xpos] == '#':
            treecount += 1
        ypos += yinc
        xpos += xinc
        if xpos >= XMAX:
            xpos -= XMAX
    return treecount

print("Part1")
print(countTrees(3,1,themap))

print("Part2")
val = countTrees(1,1,themap) * countTrees(3,1,themap) * countTrees(5,1,themap) * countTrees(7,1,themap) * countTrees(1,2,themap)
print(val)