from Population import Population
from Data import Reader

seed = 1
data = Reader()
population = Population(seed, 10, 10, data.problems, data.rooms, data.courses, data.days, data.curricula, data.periods_per_day, data.num_rooms, 10, 10)
count = 50
while population.checkGeneration(1) == False:
    population.nextGeneration()
    count = count - 1

print(" ----- CONSTRUCTION PHASE COMPLETED ----- ")
# population.showAllPerturbativeHeuristics()
population.evolvePerturbativeHeuristic()
population.applyPerturbativeHeuristics()