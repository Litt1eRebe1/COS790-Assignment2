from Population import Population
from Data import Reader

seed = 1
data = Reader()
population = Population(seed, 10, 2, data.problems, data.rooms, data.courses, data.days, data.curricula, data.periods_per_day, data.num_rooms)