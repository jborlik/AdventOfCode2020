#import itertools
#import numpy
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])


with open('day08.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".splitlines()]

class Instruction:
    def __init__(self, line):
        words = line.split(' ')
        self.ins = words[0]
        self.arg = int(words[1])
        self.callcount = 0

class Program:
    def __init__(self, data):
        self.accumulator = 0
        self.instructions = [Instruction(line) for line in data]
        self.pointer = 0
    
    def run(self):
        self.pointer = 0
        self.accumulator = 0
        self.state = 'run'

        for aIns in self.instructions:
            aIns.callcount = 0

        while self.pointer >= 0 and self.pointer < len(self.instructions):
            # execute this instruction
            aIns = self.instructions[self.pointer]

            if aIns.callcount > 0:
                # this has already been called before, i.e. this is an infinite loop
                print(f"Loop found:  ins={self.pointer} accum={self.accumulator}")
                self.state = 'loop'                
                break

            #print(f"Line {self.pointer}:  {aIns.ins} {aIns.arg}")

            if aIns.ins == 'acc':
                self.accumulator += aIns.arg
                self.pointer += 1
            elif aIns.ins == 'jmp':
                self.pointer += aIns.arg
            elif aIns.ins == 'nop':
                self.pointer += 1

            aIns.callcount += 1

        if self.state == 'run':
            self.state = 'done'

        print(f"Program terminated.  ins={self.pointer} accum={self.accumulator}")

    def highestCalled(self):
        ihighest = 0
        for i,aIns in enumerate(self.instructions):
            if aIns.callcount > 0:
                ihighest = i
        return ihighest
            

thedata = alldata
#thedata = testdata

theProgram = Program(thedata)

theProgram.run()

print("PART TWO!")

for iline,aIns in enumerate(theProgram.instructions):
    print(f"Checking line {iline}:  {aIns.ins} {aIns.arg}")
    if aIns.ins == 'nop':
        aIns.ins = 'jmp'
        theProgram.run()
        if theProgram.state == 'done':
            print(f"GOT IT.  accum={theProgram.accumulator}")
            break
        # not it
        aIns.ins = 'nop'
    elif aIns.ins == 'jmp':
        aIns.ins = 'nop'
        theProgram.run()
        if theProgram.state == 'done':
            print(f"GOT IT.  accum={theProgram.accumulator}")
            break
        # not it
        aIns.ins = 'jmp'

print("Done")        