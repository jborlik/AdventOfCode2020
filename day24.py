#import itertools
#import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time
#import pprint


with open('day24.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".splitlines()]   # 


thedata = testdata
thedata = alldata


class Hex:
    def __init__(self, q, r, s=None):
        self.q = q
        self.r = r
        if s:
            self.s = s
        else:
            self.s = -q - r
    def length(self):
        return int( (abs(self.q) + abs(self.r) + abs(self.s)) / 2)
    def __eq__(self, another):
        return self.q == another.q and self.r == another.r and self.s == another.s 
    def __hash__(self):
        return hash((self.q, self.r, self.s))
    def __str__(self):
        return f"({self.q}, {self.r}, {self.s})"

def hex_subtract(hex1:Hex, hex2:Hex):
    return Hex(hex1.q - hex2.q, hex1.r - hex2.r, hex1.s - hex2.s)

def hex_distance(hex1:Hex, hex2:Hex):
    return hex_subtract(hex1, hex2).length()

def hex_add(hex1:Hex, hex2:Hex):
    return Hex(hex1.q + hex2.q, hex1.r + hex2.r, hex1.s + hex2.s)

# 0=ne, 1=n, 2=nw, 3=sw, 4=s, 5=se
#hex_directions = [Hex(1,0),Hex(1,-1),Hex(0,-1),Hex(-1,0),Hex(-1,1),Hex(0,1)]
#hex_dirstring = ['ne','n','nw','sw','s','se']
#                   0=e,         1=ne,         2=nw,       3=w,       4=sw,       5=se
hex_directions = [Hex(1,-1,0),Hex(1,0,-1),Hex(0,1,-1),Hex(-1,1,0),Hex(-1,0,1),Hex(0,-1,1)]
hex_dirstring = ['e','ne','nw','w','sw','se']



# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------


START = time.perf_counter()

tiles = {}   # touched tiles, Hex(): 0/1  (1=black)

def followAndFlipTile(apath, tiles):
    tile = Hex(0,0)
    # walk through path, accumulating direction string if needed, and walk
    dir = ''
    for achar in apath:
        dir += achar
        if dir in hex_dirstring:
            idir = hex_dirstring.index(dir)
            tile = hex_add(tile, hex_directions[idir])  # walk!
            dir = ''
    if dir != '':
        raise f"Unknown path!:  {apath}: {dir}"
    # now we are there, so flip!
    lastval = tiles.setdefault(tile, 0)
    tiles[tile] = (lastval + 1) % 2
    print(f"Found tile {tile} and set value to {tiles[tile]}")


#followAndFlipTile("esew", tiles)
#followAndFlipTile("nwwswee", tiles)
#followAndFlipTile("nwwswee", tiles)

for aline in thedata:
    followAndFlipTile(aline, tiles)

def countTotalBlack(tiles):
    countblack = 0
    for atile, aval in tiles.items():
        countblack += (aval  % 2)
    return countblack

countblack = countTotalBlack(tiles)

print(f"Part 1:  Black tiles = {countblack}")



END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

START = time.perf_counter()

def day(tiles0):
    otherstocheck = []
    tiles1 = {}
    for atile, aval in tiles0.items():
        # inspect tiles around it
        blacks = 0
        for adir in hex_directions:
            adjtile = hex_add(atile, adir)
            if adjtile in tiles0:
                blacks += tiles0[adjtile]
            else:
                otherstocheck.append(adjtile)
        if aval == 1:  # if black
            if blacks == 0 or blacks > 2:
                pass  # don't add it back
            else:
                tiles1[atile] = 1
        else: # if white
            if blacks == 2:
                tiles1[atile] = 1
    # okay, those were the existing ones, but we need to check for expansion into white
    for atile in otherstocheck:
        # inspect around it, but don't bother adding back
        blacks = 0
        for adir in hex_directions:
            adjtile = hex_add(atile, adir)
            if adjtile in tiles0:
                blacks += tiles0[adjtile]
        if blacks == 2:
            tiles1[atile] = 1
    return tiles1


for i in range(100):
    tiles = day(tiles)
    count = countTotalBlack(tiles)
    print(f"Day {i+1} count = {count}")





END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")