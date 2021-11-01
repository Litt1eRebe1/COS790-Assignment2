import random
from Evaluator import Evaluator

class Population:
    def __init__(self, seed, max_depth, num_individuals, problems, rooms, courses, days, curricula, periods_per_day, num_rooms, perturbative_max_length, num_perturbative, tournament_size = 3):
        self.problems = problems
        self.rooms = rooms
        self.courses = courses
        self.days = days
        self.curricula = curricula
        self.seed = seed
        random.seed(seed)
        self.max_depth = max_depth
        self.num_individuals = num_individuals
        self.individuals = []
        self.periods_per_day = periods_per_day
        self.num_rooms = num_rooms
        self.evaluator = Evaluator(self.seed, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day)
 

        self.tournament_size = tournament_size
       
        self.best_individual = None
        self.createPopulation()




    def print(self):
        count = 1
        for i in self.individuals:
            
            i.evaluator.print()
            print(" ================================================== + " + str(count) + " -- fitness  " + str(i.fitness) + " -- quality  " + str(i.quality) + " ================================================== + ")
            count = count + 1
            
    def printBest(self, time, seed):
        self.individuals.sort(key=lambda x: x.fitness, reverse=False)
        self.individuals.sort(key=lambda x: x.quality, reverse=False)
        i = self.individuals[0]
        self.individuals[0].evaluate()
        self.individuals[0].evaluator.print()
        
        print(" BEST TIMETABLE ================================================= -- fitness  " + str(i.fitness) + " -- quality  " + str(i.quality) + " ================================================== + \n")
        print(" ------- construction heuristic used ------- ")
        self.individuals[0].showTree()
    
        self.writeToFile(self.individuals[0].tree, i.fitness, i.quality, i, seed, time)

    def writeToFile(self, tree, fitness, quality, individual, seed, time):
        f=open("results" + str(seed) + ".txt", "a+")
        f.write("SEED: " + str(seed) + "\n")
        f.write("RUNTIME: " + str(time) + "\n")
        f.write(" BEST TIMETABLE ================================================= -- fitness  " + str(fitness) + " -- quality  " + str(quality) + " ================================================== + \n")
        i = 1
        for day in individual.evaluator.timetable.days:
            f.write("--------- DAY ( " + str(i) + " ) -----------\n")
            i = i + 1
            p = 1
            for period in day:
                f.write("\n ++++++ PERIOD ( " + str(p) + " ) ++++++\n")
                p = p + 1
                for room in period:
                    f.write(str(room) + "\n")
   



    def copyHeuristic(self, heuristic):
        copy = {
            "list": [],
            "fitness": 0
        }
        for i in range(0, len(heuristic['list'])):
            copy['list'].append(heuristic['list'][i].copy())
        copy['fitness'] = heuristic['fitness']

        return copy
    def checkGeneration(self, perc):
        
        num_acceptable = int(perc * len(self.individuals))
        for i in self.individuals:
            
            if i.fitness == 0:  
                num_acceptable = num_acceptable - 1
        
        return num_acceptable <= 0

    def nextGeneration(self):
        self.evaluatePopulation()
        self.individuals = self.applyOperators()
        self.evaluatePopulation()


    def tournamentSelection(self):
        tournament_pool = []
        for i in range(0, self.tournament_size):
            self.seed = self.seed + 1
            random.seed(self.seed)
            choice = random.randint(0, len(self.individuals) - 1)
           
            tournament_pool.append(self.individuals[choice].copy())
        tournament_pool.sort(key=lambda x: x.fitness, reverse=False)
        return tournament_pool[0]

    def applyOperators(self):
        i = 0
        new_population = []
        while i < len(self.individuals):
            self.seed = self.seed + 1
            random.seed(self.seed)
            choice = random.randint(0, 100)
            if choice <= 60 and i < len(self.individuals) - 1:
                kids = self.crossover()
                kids[0].operation = 'C'
                kids[1].operation = 'C'
                i = i + 2
            elif choice < 80:
                kids = self.mutate()
                kids[0].operation = 'M'
                i = i + 1
            else:

                kids = self.reproduce()
                kids[0].operation = 'R'
                i = i + 1

            for k in range(0, len(kids)):
                
                new_population.append(kids[k])
                
        
        return new_population

    def reproduce(self):
        parent = self.tournamentSelection()
        return [parent.copy()]

    def crossover(self):
        parent1 = self.tournamentSelection()
        parent2 = self.tournamentSelection()

        parent1.crossover(parent2)

        return [parent1, parent2]

    def mutate(self):  
        parent = self.tournamentSelection()
        parent.mutate()
        return [parent]

    def evaluatePopulation(self):
        for i in range(0, len(self.individuals)):
            self.individuals[i].evaluate()
            self.individuals[i].evaluator.courses = self.individuals[i].evaluator.copy_courses.copy()
            if self.individuals[i].fitness < self.best_individual.fitness:
                self.best_individual = self.individuals[i].copy()
            
        

    def createPopulation(self):
        for i in range(0, int(self.num_individuals / 2)):
            #grow
            new_individual = Chromosome(self.seed, self.max_depth, self.max_depth - i + 2, self.problems.copy(), self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day, self.perturbative_max_length, 1)
            # new_individual.showTree()
            self.individuals.append(new_individual)

        


        for i in range(0, int(self.num_individuals / 2)):
            #Full
            new_individual = Chromosome(self.seed, self.max_depth, self.max_depth - i + 2, self.problems.copy(), self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day, self.perturbative_max_length, 0)
            # new_individual.showTree()
            self.individuals.append(new_individual)
        self.best_individual = self.individuals[0].copy()
        self.evaluatePopulation()

class Chromosome:
    def __init__(self, seed, max_depth, depth, problems, rooms, courses, days, curricula, num_rooms, periods_per_day, perturbative_max_length = 10, choice = 0, copy = False, tree = None, evaluator = None):
        self.max_depth = max_depth
        self.depth = depth
        self.seed = seed
        self.problems = problems
        self.rooms = rooms
        self.courses = courses.copy()
        self.days = days
        self.curricula = curricula
        self.num_rooms = num_rooms
        self.periods_per_day = periods_per_day
        self.choice = choice
        self.fitness = 999999999
        if copy == False:
            self.createTree(choice)
            self.evaluator = Evaluator(self.seed, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day)
            
        else:
            self.tree = tree.copy()
            self.evaluator = evaluator.copy()
            
        
        self.perturbative_max_length = perturbative_max_length
        self.operation = "n"
        self.quality = 999999999
        
    def copy(self):
        copy = Chromosome(self.seed, self.max_depth, self.depth, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day, self.perturbative_max_length , self.choice, True, self.tree, self.evaluator)
        copy.fitness = self.fitness
        return copy

    def evaluate(self):
        self.evaluator.evaluate(self.tree)
        self.fitness = self.evaluator.calculateFitness()


    def createTree(self, choice = 0):
        if choice == 0:
      
            self.tree = Tree(self.seed, self.max_depth)
            self.tree.createFull()
        else:
           
            self.tree = Tree(self.seed, self.max_depth)
            self.tree.createGrow()
            
    def crossover(self, parent2):
        self.tree.crossover(parent2)

    def mutate(self):
        self.tree.mutate()
            
    def showTree(self):
        print("\n")
        print("--------- show tree ---------")
        self.tree.showTree(self.tree.root)

    def print(self):
        self.evaluator.print()

class Tree:
    def __init__(self, seed, max_depth = 6, tree = None):
        if tree != None:
            self.copy(tree)
        else:
            self.seed = seed
            random.seed(seed)
            self.constructor(max_depth)

    
    def createTerminalSet(self):
        self.terminal_set = []
        new_node = Node(True, "Saturation degree", 0, 'characteristics')
        self.terminal_set.append(new_node)

        new_node = Node(True, "Number of students", 1, 'characteristics')
        self.terminal_set.append(new_node)

        new_node = Node(True, "Largest degree", 2, 'characteristics')
        self.terminal_set.append(new_node)

        new_node = Node(True, "Lectures", 3, 'characteristics')
        self.terminal_set.append(new_node)

        new_node = Node(True, "Minimum number of working days", 4, 'characteristics')
        self.terminal_set.append(new_node)

        new_node = Node(True, "Room degree", 5, 'characteristics')
        self.terminal_set.append(new_node)

        new_node = Node(True, "First Period", 6, 'period')
        self.terminal_set.append(new_node)

        new_node = Node(True, "Random Period", 7, 'period')
        self.terminal_set.append(new_node)

        new_node = Node(True, "Minimum Penalty Period", 8, 'period')
        self.terminal_set.append(new_node)

    def createFuntionalSet(self):
        self.functional_set = []

        new_node = Node(False, "Select and Place", 0, 2)
        self.functional_set.append(new_node)

        new_node = Node(False, "Sort Ascending", 1, 2)
        self.functional_set.append(new_node)

        new_node = Node(False, "Sort Descending", 2, 2)
        self.functional_set.append(new_node)

        new_node = Node(False, "+", 3, 2)
        self.functional_set.append(new_node)

        

    def returnFuntionalNode(self):

        choice = random.randint(0, len(self.functional_set) - 1)   
        return self.functional_set[choice].copy()

    def returnTerminalNode(self, type = 0):

        choice = random.randint(0, len(self.terminal_set) - 1)

        return self.terminal_set[choice].copy()
        
    def constructor(self,max_depth):
        self.max_depth = max_depth
        self.root = None
        self.createTerminalSet()
        self.createFuntionalSet()
        self.depth = 0

    def copy(self):
        new_tree = Tree(self.seed, self.max_depth)
        for node in self.terminal_set:
            new_tree.terminal_set.append(node.copy())
        for node in self.functional_set:
            new_tree.functional_set.append(node.copy())

        new_tree.root = self.root.copy()

        new_tree.depth = self.depth
        new_tree.max_depth = self.max_depth
        new_tree.root = self.copyHelper(self.root)
        return new_tree

    def copyHelper(self, node):
        if node == None: # end
            return
        elif node.terminal == False:
            new_node = node.copy()
            new_node.children = []
            for i in range(0, len(node.children)):
                new_node.children.append(self.copyHelper(node.children[i]))
            return new_node
        else:
            new_node = node.copy()
            return new_node





    def createFull(self):
        self.root = self.full()

    def createGrow(self):
        self.root = self.grow()


    def full(self, level = 0, type = 0):
     
        if level == self.max_depth: #end here
            self.depth = self.max_depth
            if type == 0:
                return self.returnTerminalNode()
            else:
                return self.returnTerminalNode(1)
        elif level == 0: #root
            functional_node = self.returnFuntionalNode()
            num_children = 2 if functional_node.id == 0 else random.randint(2, 3)
            if functional_node.id == 1:
           
                if num_children == 2:
                    functional_node.children.append(self.full(level + 1, 0))
                    functional_node.children.append(self.full(level + 1, 1))
                else:
                    functional_node.children.append(self.full(level + 1, 0))
                    functional_node.children.append(self.full(level + 1, 0))
                    functional_node.children.append(self.full(level + 1, 1))
                    
            else:
                functional_node.children.append(self.full(level + 1, 0))
                functional_node.children.append(self.full(level + 1, 1))
            functional_node.num_children = num_children
            self.root = functional_node
            return self.root
        else:
            # create funtional node
            functional_node = self.returnFuntionalNode()
            num_children = 2 if functional_node.id == 0 else random.randint(2, 3)
            if functional_node.id == 1:
                if num_children == 2:
                    functional_node.children.append(self.full(level + 1, 0))
                    functional_node.children.append(self.full(level + 1, 1))
                else:
                    functional_node.children.append(self.full(level + 1, 0))
                    functional_node.children.append(self.full(level + 1, 0))
                    functional_node.children.append(self.full(level + 1, 1))
            else:
                functional_node.children.append(self.full(level + 1, 0))
                functional_node.children.append(self.full(level + 1, 1))
            functional_node.num_children = num_children
            self.depth = self.max_depth
            return functional_node

    
    def grow(self, level = 0, type = 0):
        if level == self.max_depth: #end here
            self.depth = self.max_depth
            if type == 0:
                return self.returnTerminalNode()
            else:
                return self.returnTerminalNode(1)
        elif level == 0: #root
            self.depth = 0
            self.root = self.grow(level + 1)
            return self.root
        else:
            # create funtional node
            choice = random.randint(0, 1)
            if choice == 0: #grow
                node = self.returnFuntionalNode()
                num_children = 2 if node.num_children == 2 else random.randint(2, 3)
                node.num_children = num_children
               
                if node.id == 0:
                    if num_children == 2:
                        node.children.append(self.full(level + 1, 0))
                        node.children.append(self.full(level + 1, 1))
                    else:
                        node.children.append(self.full(level + 1, 0))
                        node.children.append(self.full(level + 1, 0))
                        node.children.append(self.full(level + 1, 1))
                else:
                    node.children.append(self.grow(level + 1, 0))
                    node.children.append(self.grow(level + 1, 1))
            else:
                if level > self.depth:
                    self.depth = level
                node = self.returnTerminalNode()

            return node

    def showTree(self, node = None, level = 0):
      
        if node == None:
            pass
        elif level == 0:
            # at root
            print(node.description)  
               
            for i in range(0, len(node.children)):
                self.showTree(node.children[i], level + 1)
        elif node.terminal == True:
            for i in range(0, level + 1):
                print('-', end = '')
            print(" " + node.description)
        else:
            for i in range(0, level + 1):
                print('-', end = '')
            print(" " + node.description)
            for i in range(0, len(node.children)):
                self.showTree(node.children[i], level + 1)

    def showTreeToFile(self, file, node = None, level = 0):
      
        if node == None:
            pass
        elif level == 0:
            # at root
            file.write(node.description + "\n")  
               
            for i in range(0, len(node.children)):
                self.showTreeToFile(file, node.children[i], level + 1)
        elif node.terminal == True:
            # file.writelines("-" % l for l in range(0, level + 1))
            for i in range(0, level + 1):
                file.write("-")
            file.write(" " + node.description + "\n")
        else:
     
            for i in range(0, level + 1):
                file.write("-")
            file.write(" " + node.description + "\n")
            for i in range(0, len(node.children)):
                self.showTreeToFile(file, node.children[i], level + 1)


    def crossover(self, parent2):
        point1 = self.findCrossoverPoint()
        point2 = parent2.tree.findCrossoverPoint(point1.id)
        
        point1_copy = self.copyHelper(point1)
        point2_copy = self.copyHelper(point2)

        point1 = point2_copy
        point2 = point1_copy
      

    def mutate(self):
        found = False
        self.seed = self.seed + 1
        random.seed(self.seed)
        place = random.randint(1, self.depth)
        level = 0
        node = self.root
        while found == False:
          
            if level == self.depth:
                point = node
                found = True
            elif level == place:
                if node.terminal == False:
                    choice = random.randint(0, len(node.children) - 1)
                    point = node.children[choice]
                    found = True
                else:
                    point = node
                    found = True
            elif node.terminal == False:
                choice = random.randint(0, len(node.children) - 1)
                node = node.children[choice]
            else:
                point = node
                found = True
            level = level + 1
    
       
        grow_node = self.mutateHelper(point.copy(), 3)
        point.description = grow_node.description
        point.id = grow_node.id
        point.children = []
        for child in grow_node.children:
            point.children.append(child.copy())
        point.terminal = grow_node.terminal
        point.level = grow_node.level
        point.num_children = grow_node.num_children

    
        

    def mutateHelper(self, node, level):
        self.seed = self.seed + 1
        random.seed(self.seed)
        if level == self.max_depth: #end here
            if type == 0:
                return self.returnTerminalNode()
            else:
                return self.returnTerminalNode(1)
        elif level == 0: #root
            node = self.full(level + 1)
            return node
        else:
            # create funtional node
            choice = random.randint(0, 1)
            if choice == 0: #grow
                node = self.returnFuntionalNode()
                num_children = 2 if node.num_children == 2 else random.randint(2, 3)
                node.num_children = num_children
                if node.id == 0:
                    for i in range(0, num_children):
                        node.children.append(self.full(level + 1))
                else:
                    node.children.append(self.full(level + 1, 0))
                    node.children.append(self.full(level + 1, 1))
            else:
                if level > self.depth:
                    self.depth = level
                node = self.returnTerminalNode()

            return node


    def findCrossoverPoint(self, type = -1):
        
        place = random.randint(0, self.depth)
        point = self.findCrossPointHelper(self.root, place, type)
        return point

    def findMutatePoint(self):
        place = random.randint(1, self.depth)
        point = self.findMutatePointHelper(self.root, place)
        return point

    def findMutatePointHelper(self, node, depth, level = 0):
        if level == depth: #end
            return {
                "node": node,
                "level": level
            }
        else:
            if node.terminal == False:
                place = random.randint(0, len(node.children) - 1)
                if node.children[place].terminal == False:
                    return self.findMutatePointHelper(node.children[place], depth, level + 1)
                else:
                    return {
                    "node": node,
                    "level": level
                }
            else:
                return {
                    "node": node,
                    "level": level
                } 

    def findCrossPointHelper(self, node, depth, type = -1, level = 0):
        if type == -1:
            if level == depth: #end
                return node
            else:
                if node.terminal == False:
                    place = random.randint(0, len(node.children) - 1)
                    if node.children[place].terminal == False:
                        return self.findCrossPointHelper(node.children[place], depth, type, level + 1)
                    else:
                        return node
                else:
                        return node
        else:
            if node.id == type:
                return node

            for i in range(0, len(node.children)):
                if node.children[i].terminal == False:
                    node = self.findCrossPointHelper(node.children[i], depth, type, level + 1)
                if node != None:
                    return node




    
        




class Node:
    def __init__(self, terminal, description, idp, typep, level = 0, num_children = 0):
        self.terminal = terminal
        self.description = description
        self.id = idp
        self.num_children = num_children
        self.children = []
        self.level = level
        self.type = typep

    
    def setLevel(self, level):
        self.level = level

    def copy(self):
        copy = Node(self.terminal, self.description, self.id, self.level, self.num_children)
     

        for i in range(0, len(self.children)):
            new_child = self.children[i].copy()
            copy.children.append(new_child)

        return copy


    


