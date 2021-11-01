from Population import Population
from Data import Reader
import timeit
seed = 1020
data = Reader()
num_problem = 0
start = timeit.default_timer()
population = Population(seed, 6, 100, data.problems, data.rooms[num_problem], data.courses[num_problem], data.days[num_problem], data.curricula[num_problem], data.periods_per_day[num_problem], data.num_rooms[num_problem], 10, 50)
count = 20
while population.checkGeneration(1) == False and count > 0 :
    print("generation --- " + str(count))
    population.nextGeneration()
    count = count - 1






stop = timeit.default_timer()
population.printBest(stop - start, seed)

