import random
import math
import matplotlib.pyplot as plt
import time

# константы генетического алгоритма
P_CROSSOVER = 0.9       # вероятность скрещивания
P_MUTATION = 0.1        # вероятность мутации индивидуума
MAX_GENERATIONS = 50    # максимальное количество поколений

# флаги
MAX = 1
MIN = 0

def fitness_value(x):
  return 2*math.cos(x) - x/5

def select(population, flag):
  # используется метод отбора - турнирный отбор
  parents = []
  for n in range(len(population)):
    i1 = i2 = i3 = 0
    while i1 == i2 or i1 == i3 or i2 == i3:
      i1, i2, i3 = random.randint(0, len(population) - 1), random.randint(0, len(population) - 1), random.randint(0, len(population) - 1)
    if flag == MAX:
      parents.append(max([population[i1], population[i2], population[i3]], key=lambda ind: fitness_value(ind)))
    elif flag == MIN:
      parents.append(min([population[i1], population[i2], population[i3]], key=lambda ind: fitness_value(ind)))
  return parents
      
def crossing(parents, a, b):
  # используем скрещивание смешением
  a = 0.5
  newparents = parents[:]
  for child1, child2 in zip(newparents[::2], newparents[1::2]):
        if random.random() < P_CROSSOVER:
          p1 = min(child1, child2)
          p2 = max(child1, child2)
          child1 = random.uniform(max(a, p1 - a*(p2 - p1)), min(p2 + a*(p2 - p1), b))
          child2 = random.uniform(max(a, p1 - a*(p2 - p1)), min(p2 + a*(p2 - p1), b))    
  return newparents

def mutation(parents, a, b):
  newparents = []
  for mutant in parents:
    if random.random() < P_MUTATION:
      rg = random.gauss(mutant, 0.4 * abs(mutant))
      mutant = random.triangular(a, b, rg)
      mutant = max(mutant, a)
      mutant = min(mutant, b)
    newparents.append(mutant)
  return newparents

def loginfo(generation, population, fitness, flag):
  avg = min(fitness) + (max(fitness) - min(fitness)) / 2
  for x in population:
    if ((avg <= fitness_value(x) and flag == MAX) or (avg > fitness_value(x)) and flag == MIN):
      plt.scatter(generation, x, 10, "#00FF00")
    else:
      plt.scatter(generation, x, 10, "#FF0000")

def genetic_algorithm(a, b, flag, number_of_population):
  # создание начальной популяции
  population = list([random.uniform(a, b) for i in range(number_of_population)])
  #print(population)

  maxFitnessValues = []
  meanFitnessValues = []

  plt.xlabel('Поколение')
  plt.ylabel('Популяции')
  generationCounter = 1;
  while generationCounter < MAX_GENERATIONS:
    generationCounter += 1;
    # вычисление приспособленности для каждой популяции
    fitness = list([fitness_value(population[i]) for i in range(number_of_population)])

    # отбор самых приспособленных родителей
    parents = select(population, flag)

    # скрещивание родителей и получение новой популяции
    parents = crossing(parents, a, b)

    # мутация
    parents = mutation(parents, a, b)
    
    loginfo(generationCounter, population, fitness, flag)

    population[:] = parents

    if flag == MAX:
      answer = max(population, key=lambda ind: fitness_value(ind))
    elif flag == MIN:
      answer = min(population, key=lambda ind: fitness_value(ind))

    #print(population)

  print('ANSWER: x = ', answer, 'f(x) = ', fitness_value(answer))
  plt.show()

print("Введите значение границ отрезка для поиска решения: ")
x, y = [float(s) for s in input().split()]
if x > y:
  x, y = y, x

print("Ищем максимум или минимум ?(max or min): ")
s = input()
flag = MAX if s == "max" else MIN

print("Количество популяций генетического алгоритма: ")
num_pop = int(input())

genetic_algorithm(x, y, flag, num_pop)
