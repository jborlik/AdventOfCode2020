import itertools

with open('day01.dat') as datafile:
    alldata = [int(x.strip()) for x in datafile.readlines()]

testdata = [1721,
979,
366,
299,
675,
1456]    # should result in 514579

#alldata = testdata

TARGET = 2020

for a,b in itertools.combinations(alldata,2):
    if a+b == TARGET:
        print(f"Found {a}+{b}={TARGET}. a*b={a*b}")



for a,b,c in itertools.combinations(alldata,3):
    if a+b+c == TARGET:
        print(f"Found {a}+{b}+{c}={TARGET}. a*b*c={a*b*c}")


