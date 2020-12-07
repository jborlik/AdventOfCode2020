#import itertools
#import numpy
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])


with open('day07.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".splitlines()]

thedata = alldata
#thedata = testdata

class Bag:
    def __init__(self, color):
        self.color = color
        self.holds = []  # [(count, color)]
        self.isheldby = []
        self.totalcontained = -1   # bag and held bags, should be >=1
        
allbags = {}

def getOrCreate(color):
    global allbags
    if color not in allbags:
        allbags[color] = Bag(color)
    return allbags[color]

for aline in thedata:
    words = aline.split(' ')
    if len(words) > 2:
        color = f"{words[0]} {words[1]}"
        theBag = getOrCreate(color)
        if len(words) > 7:   # "x y bags contain no other bags."
            numothers = int((len(words)-4)/4)
            for i in range(4, len(words), 4):
                containedcolor = f"{words[i+1]} {words[i+2]}"
                num = int(words[i])
                theBag.holds.append( (num, containedcolor) )
                heldbag = getOrCreate(containedcolor)
                heldbag.isheldby.append( color )

sawalready = {}
def countHolds(nextlist):
    global sawalready
    count = 0
    for item in nextlist:
        if item not in sawalready:
            sawalready[item] = 1
            thisBag = allbags[item]
            count += 1
            count += countHolds(thisBag.isheldby)
    return count

mybag = allbags['shiny gold']

count = countHolds(mybag.isheldby)
print(f"Part 1:  {count} bags")


# now count the tree in the other direction

def countContains(nextlist):
    count = 1
    for (ic, name) in nextlist:
        abag = allbags[name]
        if abag.totalcontained == -1:
            abag.totalcontained = countContains(abag.holds)
        count += ic * abag.totalcontained
    return count

count2 = countContains(mybag.holds)

print(f"Part 2: {count2-1} bags")





