#import itertools
#import numpy as np
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
import collections
#import math
import time

with open('day16.dat') as datafile:
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

testdata2 = [x.strip() for x in """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".splitlines()]  # part 2


thedata = testdata
thedata = testdata2
thedata = alldata

#  First, parse the input
rules = {}   # name: [min0,max0,min1,max1]
myticket = []  # list
nearbytickets = []  # list of lists

re_rule = re.compile(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)')
parseState = 0
for aLine in thedata:
    if aLine == '':
        parseState += 1
    else:
        if parseState == 0:
            # parsing rules
            m = re_rule.match(aLine)
            rules[m[1]] = [ int(m[2]), int(m[3]), int(m[4]), int(m[5]) ]
            pass
        elif parseState == 1:
            # parsing my ticket
            if aLine == 'your ticket:':
                pass
            else:
                myticket = [int(num) for num in aLine.split(',')]
        elif parseState == 2:
            # parsing other tickets
            if aLine == 'nearby tickets:':
                pass
            else:
                nearbytickets.append( [int(num) for num in aLine.split(',')])


START = time.perf_counter()

def returnValidRules(rules, value):
    validrules = []
    for rulename, limits in rules.items():
        if (limits[0] <= value <= limits[1]) or (limits[2] <= value <= limits[3]):
            validrules.append(rulename)
    return validrules

errorrate = 0
validtickets = []

for iTicket, aTicket in enumerate(nearbytickets):
    goodtix = True
    ticket_options = []
    for iposition,aVal in enumerate(aTicket):
        validrules = returnValidRules(rules, aVal)
        ticket_options.append(validrules)
        if len(validrules) == 0:
            print(f"Val {aVal} (pos {iposition}) no rules good in {iTicket}")
            goodtix = False
            errorrate += aVal
    if goodtix:
        validtickets.append(ticket_options)


print(f"Part 1: errorrate = {errorrate}")
END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")

#print(validtickets)


START = time.perf_counter()

print(f"Valid rules remaining: {len(validtickets)}")

#
#iposition = 16
#for itix,atix in enumerate(validtickets):
#    print(f"Ticket {itix} pos {iposition}: {atix[iposition]}")
#
#

#exit()

pendingpositions = collections.deque(range(0,len(myticket)))
knownnames = dict.fromkeys(rules.keys(), -1)

while len(pendingpositions) > 0:
    iposition = pendingpositions.pop()
    print(f"trying position {iposition}")

    # try each name, does only one match?
    goodnames = []
    for aName,iVal in knownnames.items():
        if iVal == -1:  # skip if we already know this one
            countgood = 0
            for atix in validtickets:
                validrules = atix[iposition]
                if aName in validrules:
                    countgood += 1
            if countgood == len(validtickets):
                # we've found a name that is good across all tickets for this position
                goodnames.append(aName)
    if len(goodnames)==1:
        # we've found the _only_ one that is valid across all tickets
        print(f"found position {iposition} = {goodnames[0]}")
        knownnames[goodnames[0]] = iposition
    else:
        # try this position again later
        print(f"    pos {iposition} has {len(goodnames)}:  {goodnames}")
        pendingpositions.appendleft(iposition)
            
print(knownnames)

# print out my ticket
myvalues = {}
for aname, ival in knownnames.items():
    myvalues[aname] = myticket[ival]
    print(f"{aname} = {myticket[ival]}")

answer = 1
for aname, ival in myvalues.items():
    if aname.startswith('departure'):
        answer *= ival

print(f"Part 2: value = {answer}")

END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")