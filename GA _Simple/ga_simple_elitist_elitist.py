# -*- coding: utf-8 -*-
"""GA_Simple_Elitist_Elitist.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1voEO5fWYroioMK2XXzwRsjIoIfpQUfae

# Imports
"""

# Commented out IPython magic to ensure Python compatibility.
!pip install ipython-autotime
# %load_ext autotime

import numpy as np
import math
import statistics
import random
import secrets
from numpy.random import default_rng

"""# Global Variables"""

POPULATION = []
NEW_POPULATION = []
length_population = 100
length_chromosome = 12
rate_crossover = 90
rate_mutation = 50

"""# Class"""

class Chromosome:
  score = 0
  def __init__(self,schema):
    self.schema = schema
  
  def __str__(self):
    toString = ''
    for ind in self.schema:
      toString += ind  
    return toString

"""# Selection"""

def selection(population, new_population):
  merged_list = []
  merged_list.extend(population)
  merged_list.extend(new_population)

  merged_list.sort(key=lambda schema: schema.score, reverse = True)

  return merged_list[:len(POPULATION)]

"""# Mutation"""

def mutation(population):
  array = []

  for ind in population:
    array_2 = []
    
    for i,ind_schema in enumerate(ind.schema):
      yes = np.random.randint(0,100)
      
      if yes <= rate_mutation:
        if ind_schema == '0':
          array_2.append('1')
        elif ind_schema == '1':
          array_2.append('0')
      else:
        array_2.append(ind_schema)
  
  array.append(Chromosome(array_2))

  return array

"""# CrossOver"""

def topParents(population):
  population.sort(key=lambda schema: schema.score, reverse = True)
  re = []

  for ind in population:
    re.append(ind.schema)

  return re[:25]

def crossOver(population):
  parents = topParents(population)

  while len(NEW_POPULATION) < length_population:
    father = parents[np.random.randint(0,len(parents))]
    mother = parents[np.random.randint(0,len(parents))]   
    
    probability_crossover = np.random.randint(0,100)

    if probability_crossover <= rate_crossover:
      if father != mother:
        child = []
        cut = np.random.randint(1,length_chromosome)
        child.append(father[:cut] + mother[cut:])
        child.append(mother[:cut] + father[cut:])
        
        for downward in child: 
          NEW_POPULATION.append(Chromosome(downward))

"""# Score"""

def score(population_test):
  for ind in population_test:
    ind.score= ind.schema.count('1')

"""# Init Population"""

def random(): 
  array2 = []

  rng = default_rng()
  numbers = rng.choice(range(0, 2), size= 2, replace=False)
  
  array2.append(str(numbers[0]))
  array2.append(str(numbers[1]))
  
  return array2

def init_population():
  for _ in range(length_population):
    array = []
    for _ in range(int(length_chromosome/2)):
      array.extend(random())
    POPULATION.append(Chromosome(array))

"""# Main"""

count = 0
array_generation = []

while count < 1:
  flag = False
  generation = 0
  POPULATION.clear()
  NEW_POPULATION.clear()
  init_population()

  while True:
    score(POPULATION)
    crossOver(POPULATION)
    score(NEW_POPULATION)
    NEW_POPULATION = mutation(NEW_POPULATION)
    score(NEW_POPULATION)
    POPULATION = selection(POPULATION,NEW_POPULATION)
    NEW_POPULATION.clear()
    
    if POPULATION[0].score == length_chromosome:
      flag = True

    if flag:
      print("===================================================================")
      print(f'Individuo: {POPULATION[0].schema} e o score dele {POPULATION[0].score} generation {generation}')
      print("===================================================================")
      array_generation.append(generation)
      break
      
    generation += 1
  count += 1