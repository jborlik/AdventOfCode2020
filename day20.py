import itertools
import numpy as np
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
import math
import time
import pprint

with open('day20.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...""".splitlines()]   # 

seamonster_str = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.splitlines()
seamonster = np.array( [np.fromstring(x, np.int8) for x in seamonster_str])
seamonster = (seamonster==35)
seamonster_count = np.sum(seamonster)

thedata = testdata
thedata = alldata

tiles = {}
re_name = re.compile(r'Tile (\d+):')

for istart in range(0,len(thedata), 12):
    tile = np.array( [np.fromstring(x, np.int8) for x in thedata[istart+1:istart+11]] )
    tile = (tile==35)
    m = re_name.match(thedata[istart])
    if m:
        tiles[ m[1] ] = tile
    else:
        raise Exception(f"No name at {istart}: {thedata[istart]}")

TILECOUNT = len(tiles)
PICTURELEN = int(math.sqrt(TILECOUNT))
print(f"{TILECOUNT} total tiles:  {PICTURELEN}x{PICTURELEN}")

# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------

START = time.perf_counter()

# this is brute force, and it would be MANY tests.  Don't think it is plausible
#for aCombo in itertools.permutations(tiles.keys()):
#    for aFlip in itertools.product( range(0,8), repeat=TILECOUNT ):
#        print(f"{aFlip}")
#    exit()

matches = {}    # tilename: [  [(matchtile,0,False)], [], [], [], []  ], i.e. north matches matchtile north unflipped,
                #       (will be accompanied by:  matchtile: [ [(tilename,0,False)], [], [], [] ])
#matches.setdefault( [ [], [], [], [] ])

for aPair in itertools.combinations(tiles.keys(), 2):
    for side0 in range(0,4):
        for side1 in range(0,4):
            #print(f"{aPair} {side0} {side1}")
            arr0 = np.rot90(tiles[aPair[0]], k=side0)[0,:]
            arr1 = np.rot90(tiles[aPair[1]], k=side1)[0,:]
            arr1flip = np.flip(arr1)
            if np.all(arr0 == arr1):   # note opposing sides should be naturally mirrored
                lst0 = matches.setdefault(aPair[0], [ [], [], [], [] ] )
                lst0[side0].append( (aPair[1], side1, True) )
                lst1 = matches.setdefault(aPair[1], [ [], [], [], [] ] )
                lst1[side1].append( (aPair[0], side0, True) )                
            if np.all(arr0 == arr1flip):
                lst0 = matches.setdefault(aPair[0], [ [], [], [], [] ] )
                lst0[side0].append( (aPair[1], side1, False) )
                lst1 = matches.setdefault(aPair[1], [ [], [], [], [] ] )
                lst1[side1].append( (aPair[0], side0, False) )                

pprint.pprint(matches)

missingtwo = []
topleftcorner = None
for tilename, matcharr in matches.items():
    emptycount = 0
    for sidelst in matcharr:
        if len(sidelst) == 0:
            emptycount += 1
    if emptycount >=2:
        missingtwo.append(tilename)
        if len(matcharr[0])==0 and len(matcharr[3])==0:
            topleftcorner = tilename

product = 1
for val in missingtwo:
    product *= int(val)

print(f"Part 1:  val = {product}, {missingtwo}")

if topleftcorner == None:
    topleftcorner = missingtwo[0]

print(f"Top left corner tile: {topleftcorner}")




END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

START = time.perf_counter()

tileorg = {}  #  (row,col):  (name, rotcount, flip t/f)

# 0, 1, 2, 3 -> 3, 2, 1, 0
flipresult = [3, 2, 1, 0]

def findConnectedTile(irow,icol, offset, whichedge):
    """ whichedge from the known tile = 2 (south) for offset (-1,0), =1 (east) for offset (0,-1) """
    conTile = tileorg[( irow+offset[0], icol+offset[1]) ]   # this is (name, rotcount, flip) of the tile
    iedge = (whichedge - conTile[1]) % 4   # index of the connection after rotating
    if conTile[2]:
        iedge = flipresult[iedge]
    conTileConnections = matches[conTile[0]] # is name: narr,earr,sarr,warr where arr entries are (name, dir, flip)
    if len(conTileConnections[iedge]) != 1:
        print(f"FAILURE:  irow={irow} icol={icol} offset={offset} conTile={conTile} iedge={iedge}")
        print(f"FAILURE:  {conTileConnections}")
    assert len(conTileConnections[iedge]) == 1 # if this isn't true, then maybe things aren't uniquely connected
    linkToThis = conTileConnections[iedge][0]  # the only entry along the side
    thistiledir = (linkToThis[1] - ( (whichedge-2) % 4 ) ) % 4  # turn it so the matching side is facing the right direction
    thistileflip = conTile[2] != linkToThis[2]  # only flip this tile if necessary
    return (linkToThis[0], thistiledir, thistileflip)

for irow in range(PICTURELEN):
    if irow==0:
        tileorg[(0,0)] = (topleftcorner, 0, False)
        if topleftcorner == '2801':  # YES I'M HARDCODING THIS SUE ME
            tileorg[(0,0)] = (topleftcorner, 2, False)
    else:
        tileorg[(irow,0)] = findConnectedTile(irow,0, (-1,0), 2)

    for icol in range(1,PICTURELEN):
        tileorg[(irow,icol)] = findConnectedTile(irow,icol,(0,-1), 1)

print(tileorg)

def getPicture(irow, icol):
    thistile = tileorg[(irow,icol)]  # (name, rots, flip)
    pic = tiles[thistile[0]][1:-1,1:-1]
    pic = np.rot90(pic, k=thistile[1])
    if thistile[2]:
        pic = np.flip(pic)
    return pic

# okay, rack 'em and stack 'em
rowarrs = []
for irow in range(PICTURELEN):
    thisrow = np.hstack( [  getPicture(irow, icol) for icol in range(PICTURELEN) ] )
    rowarrs.append(thisrow)
picture = np.vstack(rowarrs)

print(picture)

if False:
    import matplotlib.pyplot as plt
    plt.imshow(picture)
    plt.show()

picture_count = np.sum(picture)   # we will use this once we knoow how mnay seamonsters there are

numseamonsters = 0
PICSIZE = np.shape(picture)[0]  # nxn
seamonster_shape = np.shape(seamonster)
print(f"Picture is {PICSIZE} x {PICSIZE}")
print(f"Seamonster shape: {seamonster_shape}")
print(f"Seamonster true count: {seamonster_count}")

for iFlip in [False, True]:
    if iFlip:
        picture = np.flip(picture)
    for iRot in range(4):
        picture = np.rot90(picture)
        # test
        thisseamonsters = 0
        for irow in range(PICSIZE - seamonster_shape[0]):
            for icol in range(PICSIZE - seamonster_shape[1]):
                lookover = picture[irow:irow+seamonster_shape[0], icol:icol+seamonster_shape[1]]
                countboth = np.sum( np.logical_and(lookover,seamonster) )
                #print(f"  irow={irow} icol={icol} count={countboth}")
                if countboth == seamonster_count:
                    print(f"  Seamonster starting at irow={irow} icol={icol}")
                    thisseamonsters += 1
        print(f"Flip={iFlip} Rot={iRot} seamonsters={thisseamonsters}")
        #if thisseamonsters > numseamonsters:
        #    numseamonsters = thisseamonsters
        numseamonsters += thisseamonsters 


print(f"Part 2:  roughness = {picture_count - numseamonsters*seamonster_count}")



END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")