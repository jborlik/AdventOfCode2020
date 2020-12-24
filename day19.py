#import itertools
#import numpy as np
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time

with open('day19.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""".splitlines()]   # 


thedata = testdata
thedata = alldata

re_1 = re.compile(r'(\d+): \"(\w)\"')
re_2 = re.compile(r'(\d+): ([\d+ ]+)\|([\d+ ]+)')
re_3 = re.compile(r'(\d+): ([\d+ ]+)')

# For reference, someone else did the rule parsing like:
#rules = {int(r.split(':')[0]):
#            [[int(x) for x in sr.split()]
#             for sr in r.split(':')[1].split('|')]
#            if '"' not in r else r[-2]
#         for r in rules}

#  parse the rule structure
class Rule:
    def __init__(self, aRule):
        m = re_1.match(aRule)
        if m:
            self.name = m[1]
            self.value = m[2]
            self.options = [ [], [] ]
        else:
            m = re_2.match(aRule)
            if m:
                self.name = m[1]
                self.value = None
                self.options = [ m[2].strip().split(' '), m[3].strip().split(' ') ]
            else:
                m = re_3.match(aRule)
                if m:
                    self.name = m[1]
                    self.value = None
                    self.options = [ m[2].strip().split(' '), [] ]
                else:
                    raise Exception(f"Unknown rule: {aLine}")

    def _matchList(self, allRules, optList, aLine):
        retval = []   # array of matched characters from aLine
        if len(optList)>=1:
            retval.extend( allRules[optList[0]]._matchPartialRule(allRules, aLine)) 
        if len(optList)>=2:
            for rule2 in optList[1:]:
                # okay we may have multiple matches from the first one, and we have to try all of them
                retval2 = []
                for amatch in retval:
                    matches = allRules[rule2]._matchPartialRule(allRules, aLine[amatch:])
                    for i,m in enumerate(matches):
                        matches[i] = m + amatch
                    retval2.extend(matches)
                retval = retval2
        return retval                


    def _matchPartialRule(self, allRules, aLine):
        if self.value != None:
            if len(aLine) == 0:
                return []
            return [1] if (aLine[0] == self.value) else []
        # We need to try out both, and potentially return both, which could have progressed a different amount
        retval = []
        for opts in self.options:
            retval.extend( self._matchList(allRules, opts, aLine) )
        return retval

    def matchRule(self, allRules, aLine):
        matches = self._matchPartialRule(allRules, aLine)
        return (len(matches) >= 1) and (matches[0] == len(aLine))
            


rules = {}
for irow, aLine in enumerate(thedata):
    if aLine == '':
        break
    rule = Rule(aLine)
    rules[rule.name] = rule

messages = thedata[irow+1:]



START = time.perf_counter()

count = 0
for iM, aMessage in enumerate(messages):
    bMatch = rules['0'].matchRule(rules, aMessage)
    count += bMatch
    print(f"Message {iM}:  {bMatch}")

print(f"Part 1:  count = {count}")

END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")




START = time.perf_counter()

rules['8'].options = [ ['42'], ['42', '8'] ]    # 8: 42 | 42 8
rules['11'].options = [ ['42', '31'], ['42', '11', '31'] ]    # 11: 42 31 | 42 11 31

count = 0
for iM, aMessage in enumerate(messages):
    bMatch = rules['0'].matchRule(rules, aMessage)
    count += bMatch
    print(f"Message {iM}:  {bMatch}")

print(f"Part 2:  count = {count}")


END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")