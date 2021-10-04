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
        self.num_perturbative = num_perturbative
        self.tournament_size = tournament_size
        self.perturbative_max_length = perturbative_max_length
        
        self.perturbativeHeuristics = []
        self.perturbative_heuristic = []

        self.createPopulation()
        self.createPerturbativeHeuristics()
        self.createPerturbativeHeuristicPopulation()


    def print(self):
        count = 1
        for i in self.individuals:
            
            i.evaluator.print()
            print(" ================================================== + " + str(count) + " -- fitness  " + str(i.fitness) + " -- quality  " + str(i.quality) + " ================================================== + ")
            count = count + 1
            


    def createPerturbativeHeuristics(self):
        new_node = Node(True, "Two violation mutation", 0, 'perturbative')
        self.perturbativeHeuristics.append(new_node)

        new_node = Node(True, "One violation mutation", 1, 'perturbative')
        self.perturbativeHeuristics.append(new_node)

        new_node = Node(True, "Random swap", 2, 'perturbative')
        self.perturbativeHeuristics.append(new_node)

        new_node = Node(True, "Row swap", 3, 'perturbative')
        self.perturbativeHeuristics.append(new_node)

        new_node = Node(True, "One violation row swap", 4, 'perturbative')
        self.perturbativeHeuristics.append(new_node)

    def createPerturbativeHeuristicPopulation(self):
        for num in range(0, self.num_perturbative):
            heuristic = []
            total_heuristic = {
                "list": [],
                "fitness": 0
            }
            length = random.randint(0, self.perturbative_max_length - 1)
            for i in range(0, length):
                self.seed = self.seed + 1
                
                random.seed(self.seed)
                choice = random.randint(0, 4)
                if choice == 0:
                    heuristic.append(self.perturbativeHeuristics[0].copy())
                elif choice == 1:
                    heuristic.append(self.perturbativeHeuristics[1].copy())
                elif choice == 2:
                    heuristic.append(self.perturbativeHeuristics[2].copy())
                elif choice == 3:
                    heuristic.append(self.perturbativeHeuristics[3].copy())
                else:
                    heuristic.append(self.perturbativeHeuristics[4].copy())
            total_heuristic['list'] = heuristic
            self.perturbative_heuristic.append(total_heuristic)
        
    def showAllPerturbativeHeuristics(self):
        print(" ==== showAllPerturbativeHeuristics ==== ")
        for i in range(0, len(self.perturbative_heuristic)):
            self.showPerturbativeHeuristic(i)

    def showPerturbativeHeuristic(self, index):
        show_list = []
        for node in self.perturbative_heuristic[index]['list']:
            show_list.append(node.description)
        
        print(" showPerturbativeHeuristic --- ")
        print(show_list)

    def applyPerturbativeHeuristics(self):
        for h in range(0, len(self.perturbative_heuristic)):
            fitness = 0
            for s in range(0, len(self.individuals)):
                old_quality = int(self.individuals[s].quality)
         
                self.individuals[s].quality = self.individuals[s].applyPerturbativeHeuristics(self.perturbative_heuristic[h]['list'])
                fitness = fitness + (old_quality - self.individuals[s].quality )
               
            self.perturbative_heuristic[h]['fitness'] = fitness

    def hillClimb(self):
        for h in range(0, len(self.perturbative_heuristic)):
            fitness = 0
            steps = 0
            improvement = True
            while improvement == True and steps < 20:
                for s in range(0, len(self.individuals)):
                    old_quality = int(self.individuals[s].quality)
                    self.individuals[s].quality = self.individuals[s].applyPerturbativeHeuristics(self.perturbative_heuristic[h]['list'])
                    fitness = fitness + (old_quality - self.individuals[s].quality )
                improvement = True if fitness > self.perturbative_heuristic[h]['fitness'] else False
                if improvement == True:
                    for s in range(0, len(self.individuals)):
                        self.individuals[s].quality = self.individuals[s].actuallyApplyPerturbativeHeuristics(self.perturbative_heuristic[h]['list'])
                self.perturbative_heuristic[h]['fitness'] = fitness
                steps = steps + 1
        print(len(self.perturbative_heuristic))
        for h in self.perturbative_heuristic:
            print("hill climb fitness: " + str(h['fitness']))

    def evolvePerturbativeHeuristic(self):
        count = 0
        temp_heuristics = []
        while count < len(self.perturbative_heuristic):
            self.seed = self.seed + 1
            random.seed(self.seed)
            choice = random.randint(0, 100)
            if choice < 55:
                kids = self.crossOverPerturbativeHeuristic()
            elif choice < 66:
                kids = self.mutatePerturbativeHeuristic(0)
            elif choice < 78:
                kids = self.mutatePerturbativeHeuristic(1)
            elif choice < 89:
                kids = self.mutatePerturbativeHeuristic(2)
            else:
                kids = self.reproducePerturbativeHeuristic()

            for k in kids:
                count = count + 1
                temp_heuristics.append(k)
        self.perturbative_heuristic = temp_heuristics
        
    def reproducePerturbativeHeuristic(self):
        heuristic = self.selectPerturbativeHeuristics()
        return [self.copyHeuristic(heuristic)]

    def hillClimb(self):
        pass
      
    def mutatePerturbativeHeuristic(self, type):
        heuristic = self.selectPerturbativeHeuristics()
        if type == 0: # add heursitc to current heauristc
            choice = random.randint(0, 4)
            heuristic['list'].append(self.perturbativeHeuristics[choice])
        elif type == 1: # remove heuristc
            if len(heuristic['list']) > 0:
                heuristic['list'].pop()
        else: # change to new heuristic
            choice = random.randint(0, 4)
            random_index = random.randint(0, len(heuristic['list']) - 1)
            heuristic['list'][random_index] = self.perturbativeHeuristics[choice]

        return [heuristic]

    def crossOverPerturbativeHeuristic(self):
        parent1 = self.selectPerturbativeHeuristics()
        parent2 = self.selectPerturbativeHeuristics()
        self.seed = self.seed + 1
        random.seed(self.seed)

        if len(parent1['list']) > len(parent2['list']): #find cross point that will work for both
            choice = random.randint(0, len(parent2['list']) - 1)
            length = len(parent1['list'])
        else:
            choice = random.randint(0, len(parent1['list']) - 1)
            length = len(parent2['list'])
        length_parent1 = len(parent1['list'])
        length_parent2 = len(parent2['list'])
        
        for i in range(choice, length):
           
            if i < length_parent1 and i < length_parent2:
                temp = parent1['list'][i].copy()
                parent1['list'][i] = parent2['list'][i].copy()
                parent2['list'][i] = temp
            elif i < length_parent1:
                temp = parent1['list'][i].copy()
                parent2['list'].append(temp)
            else:
                temp = parent2['list'][i].copy()
                parent2['list'].append(temp)
        if length_parent2 > length_parent1:
            for i in range(0, length_parent2 - length_parent1):
                del parent2['list'][-1]

        if length_parent1 > length_parent2:
            for i in range(0, length_parent1 - length_parent2):
                del parent1['list'][-1]

        return [parent1, parent2]

    def selectPerturbativeHeuristics(self):
        heuristic_pool = []
        
        for i in range(self.tournament_size):
            self.seed = self.seed + 1
            random.seed(self.seed)
            choice = random.randint(0, len(self.perturbative_heuristic) - 1)
            heuristic_pool.append(self.perturbative_heuristic[choice])

        heuristic_pool.sort(key=lambda x: x['fitness'], reverse=False)
        
        return self.copyHeuristic(heuristic_pool[0])

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
        count = 1
        for i in self.individuals:
            
            i.evaluate()
            i.evaluator.courses = i.evaluator.copy_courses.copy()
            
            count = count + 1
            

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
        if copy == False:
            self.createTree(choice)
            self.evaluator = Evaluator(self.seed, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day)
            
        else:
            self.tree = tree.copy()
            self.evaluator = evaluator.copy()
            
        
        self.perturbative_max_length = perturbative_max_length
        self.operation = "n"
        self.quality = 9999999
        
    def copy(self):
        copy = Chromosome(self.seed, self.max_depth, self.depth, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day, self.perturbative_max_length , self.choice, True, self.tree, self.evaluator)
        copy.fitness = self.fitness
        return copy

    def evaluate(self):
        self.evaluator.evaluate(self.tree)
        self.fitness = self.evaluator.calculateFitness()

    def applyPerturbativeHeuristics(self, heuristic):
        soft = self.evaluator.applyPerturbativeHeuristics(heuristic)
        return soft

    def actuallyApplyPerturbativeHeuristics(self, heuristic):
        soft = self.evaluator.actuallyApplyPerturbativeHeuristics(heuristic)
        return soft

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

        new_node = Node(False, "%", 0, 2)
        self.functional_set.append(new_node)

        new_node = Node(False, "#", 1, 3)
        self.functional_set.append(new_node)

        

    def returnFuntionalNode(self):

        choice = random.randint(0, len(self.functional_set) - 1)   
        return self.functional_set[choice].copy()

    def returnTerminalNode(self, type = 0):
        if type == 0: #"characteristics"
            choice = random.randint(0, len(self.terminal_set) - 4)
        else: #"period"
            choice = random.randint(6, len(self.terminal_set) - 1)

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
    def __init__(self, terminal, description, id, type, level = 0, num_children = 0):
        self.terminal = terminal
        self.description = description
        self.id = id
        self.num_children = num_children
        self.children = []
        self.level = level
    
    def setLevel(self, level):
        self.level = level

    def copy(self):
        copy = Node(self.terminal, self.description, self.id, self.level, self.num_children)
     

        for i in range(0, len(self.children)):
            new_child = self.children[i].copy()
            copy.children.append(new_child)

        return copy


    


