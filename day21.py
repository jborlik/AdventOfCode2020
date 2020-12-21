#import itertools
#import numpy as np
#import copy
#import re   # r = re.compile(r'xxx'), m = r.match(str), print(m[1])
#import collections
#import math
import time
import pprint


with open('day21.dat') as datafile:
    alldata = [x.strip() for x in datafile.readlines()]

testdata = [x.strip() for x in """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".splitlines()]   # 


thedata = testdata
thedata = alldata

class Food:
    def __init__(self, aLine):
        ings, algs = aLine.split('(')
        self.ingredients = [ing.strip() for ing in ings.strip().split(' ')]
        self.allergens = [ alg.strip() for alg in algs[len('contains'):-1].split(',') ]
    def __repr__(self):
        return f"Ingredients: {self.ingredients}    (contains {self.allergens} )"

foods = [ Food(aLine) for aLine in thedata ]


# ------------------------------------------------------------------------------------
#  Part 1
# ------------------------------------------------------------------------------------


START = time.perf_counter()

allergens = {}  # name: [food indexes]
for ifood, aFood in enumerate(foods):
    for aAllergen in aFood.allergens:
        lst0 = allergens.setdefault(aAllergen, [] )
        lst0.append(ifood)

class Ingredient:
    def __init__(self, name):
        self.name = name
        self.foods = []
        self.allergens = {}
    def __repr__(self):
        return f"<Ingredient {self.name} in={self.foods} allergens={self.allergens}>"

ingredients = {}  # name: Ingredient()

for ifood, aFood in enumerate(foods):
    for ingname in aFood.ingredients:
        aIng = ingredients.setdefault(ingname, Ingredient(ingname))
        aIng.foods.append(ifood)
        for aAllergen in aFood.allergens:
            numtimes = aIng.allergens.get(aAllergen, 0)
            numtimes += 1
            aIng.allergens[aAllergen] = numtimes

#print(ingredients)

# now lets remove as many allergen labels from ingredients that we can
# each ingredient needs to be in _all_ foods where an allergen is given, or it isn't that allergen
for allergen_name, allergen_foods in allergens.items():

    for ing_name, aIngredient in ingredients.items():

        if allergen_name in aIngredient.allergens.keys():
            check = all(food in aIngredient.foods for food in allergen_foods)
            if not check:
                del aIngredient.allergens[allergen_name]


pprint.pprint(ingredients)

count_clean_ingredient_appearances = 0
for ing_name, aIngredient in ingredients.items():
    if len(aIngredient.allergens) == 0:
        count_clean_ingredient_appearances += len(aIngredient.foods)

print(f"Part 1:  number of clean ingredient appearances: {count_clean_ingredient_appearances}")



END = time.perf_counter()
print(f"Time taken for part 1: {END - START} seconds")


# ------------------------------------------------------------------------------------
#  Part 2
# ------------------------------------------------------------------------------------

START = time.perf_counter()

# Loop through here again
allergen_ingredient = {}  # allergen_name: ingredient_name for sure

while len(allergen_ingredient) != len(allergens):
    for ing_name, aIngredient in ingredients.items():
        if len(aIngredient.allergens)==1:
            # do we have this one yet?
            allergen_name = list(aIngredient.allergens.keys())[0]
            if not (allergen_name in allergen_ingredient.keys()):
                # not here, so add it and remove from all other ingredients
                allergen_ingredient[allergen_name] = ing_name
                for ing_check, anotherIngredient in ingredients.items():
                    if ing_check != ing_name:
                        if allergen_name in anotherIngredient.allergens.keys():
                            del anotherIngredient.allergens[allergen_name]

pprint.pprint(allergen_ingredient)

print("Part2:  ", end='')
for key, value in sorted(allergen_ingredient.items(), key=lambda x: x[0]): 
    print("{},".format(value), end='')
print()


END = time.perf_counter()
print(f"Time taken for part 2: {END - START} seconds")