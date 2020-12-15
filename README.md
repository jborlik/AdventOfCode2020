# AdventOfCode2020

Python code to solve daily puzzles of http://adventofcode.com/2020

Code is tested with Python 3.8.3 (Anaconda distribution) on Win10. Developed with VSCode.

## Days

* Day 1:  Use of itertools.combintations makes this one easy.  I got to it late (due to server crashes), but it took only a couple of minutes.
* Day 2:  Regex to parse the input string, then loop through and evaluate each item to meet the different password validity rules.  Fumbled around with the regex for a while, because I haven't used it recently.  Part 1: 00:23:47, rank 4973.  Part 2: 00:31:34, rank 4673.
* Day 3:  Count "trees" by walking through a 2D array with various "slopes".  Part 1: 00:06:25, rank 1123.  Part 2: 00:12:33, rank 1477.  Not sure if I could have done it much faster, although someone got part 1 in 35 seconds!
* Day 4:  Parse a document, separate into sets of key/value pairs, and then check the validity of each set (passport) against several rules.  I fumbled the initial parsing and had trouble figuring out the problem, which ended up being that I was forgetting to add in the last set at the end of the file.  Part 1: 00:42:40, rank 7447.  Part 2: 01:06:41, rank 4820.
* Day 5:  Part 1 was easy.  For part 2, find the missing seat, given a list of taken seats.  I ended up making a dict of (row,col) and the deleting the keys that were taken.  My time was a bit worse on part 2 because I accidentally didn't iterate over the right number (use a constant!).  Part 1:  00:12:22, rank 1811.  Part 2: 00:30:41, rank 3917.
* Day 6:  Used a dict to accumulate values, to help with uniqueness.  This was a bit more work in part 1, but made part 2 easier.  Part 1: 00:11:27, rank 4294.  Part 2: 00:18:48, rank 3392.
* Day 7:  This one had more typing.  Built a tree with nodes that contained pointers up and down.  Part 1 counted up the tree, and part 2 counted down the tree.  Part 1:  00:45:08, rank 4076.  Part 2: 00:55:52, rank 2981.
* Day 8:  List of operations that alter a state variable and an op pointer.  Classic AoC.  Took a bit to get the machinery in place.  Part 2 involved trying to find a single op that was corrupted and resulting in an infinite loop.  It took me a bit to realize that one could just brute force it... Just iterate through each line, alter it, re-try the program and stop if the program completes.  Part 1: 00:19:54, rank 5264.  Part 2: 00:41:43, rank 4602.
* Day 9:  Part 1 used itertools.permutations check for validity over a moving window of a list.  Part 2 iterated over the list again, to find a contiguous window that summed to a value.  Brute force seemed good enough.  Part 1: 00:12:09 rank 2879.  Part 2: 00:24:01 rank 3033.
* Day 10:  Part 1 was just calling the right numpy function (np.diff).  Part 2 required some thought!  And I ended up [needing help]( https://github.com/neelakantankk/Advent_of_Code_2020/blob/main/Day_10/day_10.py).  Part 1: 00:14:19, rank 4074.  Part 2: 22:18:43, rank 30446.
* Day 11:  A character matrix with rules to change the character state.  The rules involved looking at the neighbors at each character.  Part 2 gave it a twist by requiring looking an arbitrary distance in the eight directions.  Part 1: 00:44:00, rank 3824.  Part 2: 01:06:34, rank 3263.
* Day 12:  Movement on a grid based on commands, requiring left/right rotations.  Another classic AoC.  It would be useful to have the direction arrays and approach (x % y for list rotation) set up ahead of time.  Part 1: 00:32:03 rank 4441.  Part 2: 00:51:43 rank 3354.
* Day 13:  Modulo algebra!  Part 1 was straightforward, just had a cycle through a list.  Part 2 was quite a bit trickier.  I tried a brute-force solution, and ran it overnight (!) without it returning.  The insight (the next day) was that once one identified a time for a pair of buses, that pattern would repeat with the least common multiple of the pair.  So one could then take that aggregated cycle to match with another bus.  This completed successfully in 0.008 sec.  Part 1:  00:18:54, rank 4150.  Part 2: 16:27:24, rank 18332.
* Day 14:  Bit arithmetic!  Part 1 was straightforward (as usual?), with a computation of two masks (one to set bits and one to clear bits), and then the application over a list of numbers.  Part 2 had a twist (as usual?), with a varying set of bit positions that would have to be set to all possible values (i.e. sometimes two bits, 00 01 10 11, and sometimes more).  I solved that by using yet another bitmask, iterating from 0 to 2**n, and then setting/unsetting the particular bits based on this mask.  Part 1:  00:26:06, rank 2343.  Part 2: 01:08:23, rank 2796.  Honestly, it isn't a bad hour or so to put into this, and even if my times are not competitive, it is still a sense of satisfaction in figuring out the puzzle.
* Day 15:  A simple rules-based sequence, requiring the tracking of the last time a number was referenced.  Python made this easy, as one could use a dict to store and lookup the last time a value was used (rather than keeping track of the entire sequence).  Part 2 extended out to 30M turns, and my solution took 12.4 sec to run.  (I wonder if there was a cycle somewhere which would allow termination earlier?) This was also the first sub-1000 (leaderboard!) finish for me this year!  Part 1: 00:18:21 rank 1800, part 2: 00:20:21 rank 884.  




## See previous work at:
* https://github.com/jborlik/AdventOfCode2015
* https://github.com/jborlik/AdventOfCode2016
* https://github.com/jborlik/AdventOfCode2017
* https://github.com/jborlik/AdventOfCode2018
* https://github.com/jborlik/AdventOfCode2019
