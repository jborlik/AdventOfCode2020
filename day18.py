#import itertools
#import numpy as np
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time
import enum

with open('day18.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """1 + (2 * 3) + (4 * (5 + 6))
1 + 2 * 3 + 4 * 5 + 6
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
""".splitlines()]   # 51, 71, 26, 437, 12240, 13632


thedata = testdata
thedata = alldata

# taken from:  https://github.com/gnebehay/parser/blob/master/parser.py

class ExpTokenType(enum.Enum):
    T_NUM = 0
    T_PLUS = 1
    T_MINUS = 2
    T_MULT = 3
    T_DIV = 4
    T_LPAR = 5
    T_RPAR = 6
    T_END = 7

class ExpNode:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
        self.children = []

def lexical_analysis(s):
    mappings = {
        '+': ExpTokenType.T_PLUS,
        '-': ExpTokenType.T_MINUS,
        '*': ExpTokenType.T_MULT,
        '/': ExpTokenType.T_DIV,
        '(': ExpTokenType.T_LPAR,
        ')': ExpTokenType.T_RPAR}

    tokens = []
    for c in s:
        if c in mappings:
            token_type = mappings[c]
            token = ExpNode(token_type, value=c)
        elif re.match(r'\d', c):
            token = ExpNode(ExpTokenType.T_NUM, value=int(c))
        elif c == ' ':
            continue
        else:
            raise Exception('Invalid token: {}'.format(c))
        tokens.append(token)
    tokens.append(ExpNode(ExpTokenType.T_END))
    return tokens

def evaluateTokens(tokens, startIndex):
    """Evaluate through this level of the token list, starting with startIndex.
       Note that when we get to a T_LPAR, we will recurse.
       When we get to a T_RPAR or T_END, we will return the accumulated value as
          well as the index we were on."""
    index = startIndex
    value = 0
    activeOperator = ExpTokenType.T_PLUS
    while index < len(tokens):
        aToken = tokens[index]
        if aToken.token_type == ExpTokenType.T_NUM:
            if activeOperator == ExpTokenType.T_PLUS:
                value += aToken.value
            elif activeOperator == ExpTokenType.T_MULT:
                value *= aToken.value
        elif aToken.token_type in [ExpTokenType.T_PLUS, ExpTokenType.T_MULT]:
            activeOperator = aToken.token_type
        elif aToken.token_type == ExpTokenType.T_LPAR:
            subvalue, index = evaluateTokens(tokens, index+1)
            if activeOperator == ExpTokenType.T_PLUS:
                value += subvalue
            elif activeOperator == ExpTokenType.T_MULT:
                value *= subvalue
        elif aToken.token_type in [ExpTokenType.T_RPAR, ExpTokenType.T_END]:
            return value, index
        else:
            raise Exception(f'Invalid token: {aToken.token_type} {aToken.value}')
        index += 1


def evaluateExpression(aLine):
    tokens = lexical_analysis(aLine)
    value, _ = evaluateTokens(tokens, 0)
    return value



START = time.perf_counter()

sumvals = 0
for i,aLine in enumerate(thedata):
    val = evaluateExpression(aLine)
    print(f"Line {i}:  val = {val}")
    sumvals += val

print(f"Part 1:  sum = {sumvals}")

#tests should say:  # 51, 71, 26, 437, 12240, 13632

END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")



def evaluateTokens2(tokens, startIndex):
    """Evaluate through this level of the token list, starting with startIndex.
       We need to give addition a higher priority than multiplication!

       Note that when we get to a T_LPAR, we will recurse.
       When we get to a T_RPAR or T_END, we will return the accumulated value as
          well as the index we were on.
          
       For this part, we will accumulate all of the tokens at this level (resolving
          parathenses, and then process them to ensure that the "addition" units
          are done first.
          """
    index = startIndex
    levelNodes = []
    while index < len(tokens):
        aToken = tokens[index]

        if aToken.token_type in [ExpTokenType.T_PLUS, ExpTokenType.T_MULT, ExpTokenType.T_NUM]:
            levelNodes.append(aToken)
        
        elif aToken.token_type in [ExpTokenType.T_END, ExpTokenType.T_RPAR]:
            # stop and process the level nodes, to return
            break

        elif aToken.token_type == ExpTokenType.T_LPAR:
            subvalue, index = evaluateTokens2(tokens, index+1)
            # insert this resolved value into the level list
            levelNodes.append(ExpNode(ExpTokenType.T_NUM, value=subvalue))

        else:
            raise Exception(f'Invalid token: {aToken.token_type} {aToken.value}')
        index += 1

    # okay, we now have a list of NUM / OP / NUM / OP / NUM that can be resolved
    # the T_PLUS/T_NUM pairs need to be resolved first
    value = 0
    multVals = []
    assert levelNodes[0].token_type == ExpTokenType.T_NUM
    lastVal = levelNodes[0].value
    for i in range(1,len(levelNodes)-1,2):
        opNode = levelNodes[i]
        assert levelNodes[i+1].token_type == ExpTokenType.T_NUM
        if opNode.token_type == ExpTokenType.T_PLUS:
            lastVal += levelNodes[i+1].value
        elif opNode.token_type == ExpTokenType.T_MULT:
            multVals.append(lastVal)
            lastVal = levelNodes[i+1].value
        else:
            raise Exception(f'Invalid token type while resolving level:  {opNode.token_type}')
    multVals.append(lastVal)
    # okay, additions resolved
    value = 1
    for aVal in multVals:
        value *= aVal
    return value, index


def evaluateExpression2(aLine):
    tokens = lexical_analysis(aLine)
    value, _ = evaluateTokens2(tokens, 0)
    return value






START = time.perf_counter()


sumvals = 0
for i,aLine in enumerate(thedata):
    val = evaluateExpression2(aLine)
    print(f"Line {i}:  val = {val}")
    sumvals += val

print(f"Part 1:  sum = {sumvals}")


END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")