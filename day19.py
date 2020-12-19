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

    def _matchList(self, allRules, optList, aLine) -> int:
        index = 0
        for rulenum in optList:
            thisone = allRules[rulenum]._matchPartialRule(allRules, aLine[index:])
            if thisone == 0:
                return 0
            index += thisone
        return index

    def _matchPartialRule(self, allRules, aLine) -> int:
        if self.value != None:
            return 1 if (aLine[0] == self.value) else 0
        for opts in self.options:
            count = self._matchList(allRules, opts, aLine)
            if count != 0:
                return count
        return 0

    def matchRule(self, allRules, aLine):
        count = self._matchPartialRule(allRules, aLine)
        return count == len(aLine)
            


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




END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")