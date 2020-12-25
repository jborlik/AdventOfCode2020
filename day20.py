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
        if len(matcharr[2])==0 and len(matcharr[3])==0:
            topleftcorner = tilename

product = 1
for val in missingtwo:
    product *= int(val)

print(f"Part 1:  val = {product}, {missingtwo}")

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
#flipresult = [3, 2, 1, 0]
flipresult = [2, 1, 0, 3]


def portDir( idir, irot, flipped):
    """ finds internal index for a desired direction idir, given rotation and flip """
    theport = (idir + irot) % 4
    if flipped:
        theport = flipresult[theport]
    return theport

def getOrgTileConnection( irow, icol, idir):
    """iport=0,1,2,3 n,e,s,w, in the actual positioned tile frame
       returns the tile connections for that port"""
    theTile = tileorg[ (irow, icol) ]
    assert theTile != None  # we haven't placed that tile yet?
    theport = portDir(idir, theTile[1], theTile[2])
    return matches[theTile[0]][theport]


def getPicture(irow, icol):
    thistile = tileorg[(irow,icol)]  # (name, rots, flip)
    pic = tiles[thistile[0]][1:-1,1:-1]
    if thistile[2]:
        pic = np.flipud(pic)    
    pic = np.rot90(pic, k=thistile[1])
    return pic

def findConnectedTile(irow,icol, offset, whichedge):
    """ whichedge from the known tile = 2 (south) for offset (-1,0), =1 (east) for offset (0,-1) """
    conTile = tileorg[( irow+offset[0], icol+offset[1]) ]   # this is (name, rotcount, flip) of the tile
    iedge = (whichedge + conTile[1]) % 4   # index of the connection after rotating
    if conTile[2]:
        iedge = flipresult[iedge]
    conTileConnections = matches[conTile[0]] # is name: narr,earr,sarr,warr where arr entries are (name, dir, flip)
    if len(conTileConnections[iedge]) != 1:
        print(f"FAILURE:  irow={irow} icol={icol} offset={offset} conTile={conTile} iedge={iedge}")
        print(f"FAILURE:  {conTileConnections}")
    assert len(conTileConnections[iedge]) == 1 # if this isn't true, then maybe things aren't uniquely connected
    linkToThis = conTileConnections[iedge][0]  # the only entry along the side
    thistileflip = conTile[2] != linkToThis[2]  # only flip this tile if necessary
    thistiledir = (linkToThis[1] - ( (whichedge-2) % 4 ) ) % 4  # turn it so the matching side is facing the right direction
    if thistileflip:
        thistiledir = flipresult[thistiledir]
    return (linkToThis[0], thistiledir, thistileflip)

def findConnectedTile2(irow, icol, northOrg, westOrg):
    northmatch = []
    northflip = False
    westmatch = []
    westflip = False
    thistilename = ''
    if northOrg:
        connhere = getOrgTileConnection(irow-1, icol, 2) # southbound
        assert len(connhere) == 1
        connhere = connhere[0]
        thistilename = connhere[0]
        northmatch = [northOrg[0]]
        northflip = connhere[2] != northOrg[2]
    if westOrg:
        connhere = getOrgTileConnection(irow, icol-1, 1) # eastbound
        assert len(connhere) == 1
        connhere = connhere[0]
        assert len(thistilename)==0 or thistilename == connhere[0]
        if len(thistilename)==0:
            thistilename = connhere[0]
        westmatch = [westOrg[0]]
        westflip = connhere[2] != westOrg[2]
    # we should know whether or not we need to flip from the connections
    thistileflip = westflip or northflip
    # now find the rotation that gives us the 
    thistileflip = True
    connections = matches[thistilename]
    gotit = False
    for irot in range(4):
        north = connections[portDir(0,irot,True)]
        if len(north) > 0:
            north = [ north[0][0] ]
        west = connections[portDir(3,irot,True)]
        if len(west) > 0:
            west = [ west[0][0] ]
        if (north == northmatch) and (west == westmatch):
            gotit = True
            break
    if not gotit:
        thistileflip = False
        for irot in range(4):
            north = connections[portDir(0,irot,thistileflip)]
            if len(north) > 0:
                north = [ north[0][0] ]
            west = connections[portDir(3,irot,thistileflip)]
            if len(west) > 0:
                west = [ west[0][0] ]
            if (north == northmatch) and (west == westmatch):
                gotit = True
                break
        if not gotit:
            raise f"Tile at {irow},{icol} named {thistilename} can't figure out how to match.  {connections}"

    return (thistilename, irot, thistileflip)


        


    
    




for irow in range(PICTURELEN):
    if irow==0:
        connections = matches[topleftcorner]
        flip = True
        gotit = False
        for irot in range(4):
            if len(connections[flipresult[(0+irot)%4]])==0 and len(connections[flipresult[(3+irot)%4]])==0:
                gotit = True
                break
        if not gotit:
            flip = False
            for irot in range(4):
                if len(connections[(0+irot)%4])==0 and len(connections[(3+irot)%4])==0:
                    gotit = True
                    break
            if not gotit:
                raise f"Top level tile {topleftcorner} can't be flipped into position: {connections}"

        tileorg[(0,0)] = (topleftcorner, irot, flip)
        print(f"(0,0) = {topleftcorner} rotated={irot} flip={flip}")

#        print(f"(0,0) n: {getOrgTileConnection(0,0,0)}")
#        print(f"(0,0) e: {getOrgTileConnection(0,0,1)}")
#        print(f"(0,0) s: {getOrgTileConnection(0,0,2)}")
#        print(f"(0,0) w: {getOrgTileConnection(0,0,3)}")

#        p1 = getPicture(0,0)
#        print(p1*1)
#        exit()



    else:
        tileorg[(irow,0)] = findConnectedTile2(irow,0, tileorg[(irow-1,0)], None)
        print(f"({irow},0) = {tileorg[(irow,0)][0]} rotated={tileorg[(irow,0)][1]} flip={tileorg[(irow,0)][2]}")

    for icol in range(1,PICTURELEN):
        northOrg = None
        if irow > 0:
            northOrg = tileorg[(irow-1, icol)]
        tileorg[(irow,icol)] = findConnectedTile2(irow,icol,northOrg, tileorg[(irow, icol-1)])

        print(f"{irow},{icol} = {tileorg[(irow,icol)]}")
        print(f"  {irow},{icol} n = {getOrgTileConnection(irow,icol,0)}")
        print(f"  {irow},{icol} e = {getOrgTileConnection(irow,icol,1)}")
        print(f"  {irow},{icol} s = {getOrgTileConnection(irow,icol,2)}")
        print(f"  {irow},{icol} w = {getOrgTileConnection(irow,icol,3)}")

print(tileorg)



# okay, rack 'em and stack 'em
rowarrs = []
for irow in range(PICTURELEN):
    thisrow = np.hstack( [  getPicture(irow, icol) for icol in range(PICTURELEN) ] )
    rowarrs.append(thisrow)
picture = np.vstack(rowarrs)

print(picture*1)


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
        picture = np.flipud(picture)
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
        if thisseamonsters > numseamonsters:
            numseamonsters = thisseamonsters
        #numseamonsters += thisseamonsters 


print(f"Part 2:  roughness = {picture_count - numseamonsters*seamonster_count}")



END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")