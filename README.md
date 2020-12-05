# AdventOfCode2020

Python code to solve daily puzzles of http://adventofcode.com/2020

Code is tested with Python 3.8.3 (Anaconda distribution) on Win10. Developed with VSCode.

## Days

* Day 1:  Use of itertools.combintations makes this one easy.  I got to it late (due to server crashes), but it took only a couple of minutes.
* Day 2:  Regex to parse the input string, then loop through and evaluate each item to meet the different password validity rules.  Fumbled around with the regex for a while, because I haven't used it recently.  Part 1: 00:23:47, rank 4973.  Part 2: 00:31:34, rank 4673.
* Day 3:  Count "trees" by walking through a 2D array with various "slopes".  Part 1: 00:06:25, rank 1123.  Part 2: 00:12:33, rank 1477.  Not sure if I could have done it much faster, although someone got part 1 in 35 seconds!
* Day 4:  Parse a document, separate into sets of key/value pairs, and then check the validity of each set (passport) against several rules.  I fumbled the initial parsing and had trouble figuring out the problem, which ended up being that I was forgetting to add in the last set at the end of the file.  Part 1: 00:42:40, rank 7447.  Part 2: 01:06:41, rank 4820.
* Day 5:  Part 1 was easy.  Find the missing seat, given a list of taken seats.  I ended up making a dict of (row,col) and the deleting the keys that were taken.  My time was a bit worse on part 2 because I accidentally didn't iterate over the right number (use a constant!).  Part 1:  00:12:22, rank 1811.  Part 2: 00:30:41, rank 3917.

## See previous work at:
* https://github.com/jborlik/AdventOfCode2015
* https://github.com/jborlik/AdventOfCode2016
* https://github.com/jborlik/AdventOfCode2017
* https://github.com/jborlik/AdventOfCode2018
* https://github.com/jborlik/AdventOfCode2019
