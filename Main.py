from Population import Population
from Data import Reader

seed = 1
data = Reader()
num_problem = 0

population = Population(seed, 3, 5, data.problems, data.rooms[num_problem], data.courses[num_problem], data.days[num_problem], data.curricula[num_problem], data.periods_per_day[num_problem], data.num_rooms[num_problem], 10, 10)
count = 0
while count < 1:
    population.nextGeneration()
    count = count + 1

print(" ----- GENERATION PHASE COMPLETED ----- ")
population.evolvePerturbativeHeuristic()
population.createForGHP(1)
population.evaluateGHP()

# num_permutations = 20
# for i in range(0, num_permutations):
#     population.hillClimb()

