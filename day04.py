#import itertools
#import numpy
#import copy
import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])

passports = []

emptylines = 0

validfields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

re_hcl = re.compile(r'#[0-9a-f]{6}$')
re_pid = re.compile(r'[0-9]{9}$')

with open('day04.dat') as datafile:

    currentstr = ''
    for aline in datafile.readlines():
        aline = aline.strip()
        if aline == '':
            passports.append(currentstr.strip())
            currentstr = ''
            emptylines += 1
        else:
            currentstr += aline + ' '

    if len(currentstr) > 0:
        passports.append(currentstr.strip())



def isValidPassportStr(astring, checkExtraValidity):
    items = astring.split(' ')

    if checkExtraValidity:
        for item in items:
            if not (item[0:3] in validfields):
                print(f"Invalid field: {item} in {astring}")
                return False
            
            [key, val] = item.split(':')
            if key == 'byr':
                vval = int(val)
                if vval < 1920 or vval > 2002:
                    return False
            elif key == 'iyr':
                vval = int(val)
                if vval < 2010 or vval > 2020:
                    return False
            elif key == 'eyr':
                vval = int(val)
                if vval < 2020 or vval > 2030:
                    return False
                pass
            elif key == 'hgt':
                unit = val[-2:]
                if unit == 'cm':
                    vval = int(val[:-2])
                    if vval < 150 or vval > 193:
                        return False
                elif unit == 'in':
                    vval = int(val[:-2])
                    if vval < 59 or vval > 76:
                        return False
                else:
                    return False
                pass
            elif key == 'hcl':
                if not re_hcl.match(val):
                    return False
                pass
            elif key == 'ecl':
                ecllist = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
                if not (val in ecllist):
                    return False
                pass
            elif key == 'pid':
                if not re_pid.match(val):
                    return False
                pass

    if len(items) == 8:
        return True
    elif len(items) == 7:
        # need to check if the missing one is cid
        for item in items:
            if (len(item) > 3) and (item[0:3]=='cid'):
                return False   # if cid is there then something else is missing
        return True  # only cid is missing
    else:
        return False 

testpassports = [
'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm',
'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929',
'hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm',
'hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in',
]

#passports = testpassports

countvalid = 0
for p in passports:
    countvalid += isValidPassportStr(p, checkExtraValidity=False)

print(f"Passport count={len(passports)}")

print(f"Part 1:  Valid passports={countvalid}")

invalidpassports = [
'eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
'iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946',
'hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
'hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007',
'pid:0874997041 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f'
]
for p in invalidpassports:
    print(isValidPassportStr(p, checkExtraValidity=True))


countvalid = 0
for p in passports:
    countvalid += isValidPassportStr(p, checkExtraValidity=True)

print(f"Part 2: Valid count={countvalid}")


