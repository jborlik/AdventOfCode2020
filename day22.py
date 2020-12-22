import itertools
import numpy as np
import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
import collections
#import math
import time
import pprint


with open('day22.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".splitlines()]   # 


thedata = testdata
thedata = alldata

decks = [ collections.deque(), collections.deque() ]

#  Parse
iplayer = 0
for aline in thedata:
    if aline == '':
        iplayer += 1
    elif aline.startswith('Player'):
        pass  # ignore because the blank line will work
    else:
        decks[iplayer].append( int(aline) )

#pprint.pprint(decks)
original_decks = copy.deepcopy(decks)

# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------

def round():
    print(f"Player 0's deck:  {decks[0]}")
    print(f"Player 1's deck:  {decks[1]}")
    card0 = decks[0].popleft()
    card1 = decks[1].popleft()
    if card0 > card1:
        print(f"Player 0 wins round")
        decks[0].append(card0)
        decks[0].append(card1)
    elif card1 > card0:
        print(f"Player 1 wins round")
        decks[1].append(card1)
        decks[1].append(card0)

START = time.perf_counter()

iround = 0
while len(decks[0]) > 0 and len(decks[1]) > 0:
    iround += 1
    print(f"Round {iround}")
    round()

winner = 0 if len(decks[0]) > 0 else 1


print(f"Part 1:  After {iround} rounds, player {winner} wins")
print(decks[winner])

score = np.dot( np.array(decks[winner]), np.arange(len(decks[winner]), 0, -1, dtype=int) )
print(f"Part 1:  Score = {score}")


END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

def game2(decks):
    """ """
    iround = 0
    previous_rounds = []  # each entry will be deepcopied decks
    while len(decks[0]) > 0 and len(decks[1]) > 0:
        iround += 1
        #print(f"Round {iround}.\nPlayer 0's deck:  {decks[0]}")
        #print(f"Player 1's deck:  {decks[1]}")        

        # check previous rounds
        for previous_config in previous_rounds:
            if previous_config[0] == decks[0] and previous_config[1] == decks[1]:
                return (0, decks[0])

        previous_rounds.append(copy.deepcopy(decks))

        # okay, play the game
        cards = [  decks[0].popleft(),  decks[1].popleft() ]

        if cards[0] <= len(decks[0]) and cards[1] <= len(decks[1]):
            # recursive combat!!
            #print(".... recursing...")
            deck0_to_send = itertools.islice(decks[0], cards[0])
            deck1_to_send = itertools.islice(decks[1], cards[1])
            winner, _ = game2( [ collections.deque( deck0_to_send ),
                                 collections.deque( deck1_to_send ) ] )
            #print(f"Anyway, player {winner} wins recursive round")
            decks[winner].append(cards[winner])
            decks[winner].append(cards[ 1-winner ])
        elif cards[0] > cards[1]:
            #print(f"Player 0 wins round")
            decks[0].append(cards[0])
            decks[0].append(cards[1])
        elif cards[1] > cards[0]:
            #print(f"Player 1 wins round")
            decks[1].append(cards[1])
            decks[1].append(cards[0])

    winner = 0 if len(decks[0]) > 0 else 1
    return (winner, decks[winner])



START = time.perf_counter()

decks = copy.deepcopy(original_decks)
winner, windeck = game2(decks)

print(f"Part 2:  Winner is {winner}")
print(windeck)


score = np.dot( np.array(windeck), np.arange(len(windeck), 0, -1, dtype=int) )
print(f"Part 2:  Score = {score}")




END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")