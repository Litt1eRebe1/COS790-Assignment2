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
            self.perturbative_heuristic.append(heuristic)
        

    def showPerturbativeHeuristic(self, index):
        show_list = []
        for node in self.perturbative_heuristic[index]:
            show_list.append(node.description)
        print("HEURISTIC")
        print(show_list)

    def mutatePerturbativeHeuristic(self):
        pass

    def crossOverPerturbativeHeuristic(self):
        pass
    

    def nextGeneration(self):
        self.evaluatePopulation()
        self.applyOperators()

    def tournamentSelection(self):
        # print("-......... tournamet START ..........")
        tournament_pool = []
        for i in range(0, self.tournament_size):
            self.seed = self.seed + 1
            random.seed(self.seed)
            choice = random.randint(0, len(self.individuals) - 1)
           
            tournament_pool.append(self.individuals[choice].copy())
        tournament_pool.sort(key=lambda x: x.fitness, reverse=True)
        # print("-......... tournamet END ..........")
        return tournament_pool[0]

    def applyOperators(self):
        self.seed = self.seed + 1
        random.seed(self.seed)
        choice = random.randint(0, 100)
        if choice <= 80:
            self.crossover()
        else:
            self.mutate()

    def crossover(self):
        print("---------------CROOSSS START --------------->")
        parent1 = self.tournamentSelection()
        parent2 = self.tournamentSelection()

        parent1.crossover(parent2)
        print("--------------- --------------- CROOSSS END --------------->")

    def mutate(self):
        pass

    def evaluatePopulation(self):
        for i in self.individuals:
            i.evaluate()
            

    def createPopulation(self):
        for i in range(0, int(self.num_individuals / 2)):
            #grow
            new_individual = Chromosome(self.seed, self.max_depth, self.max_depth - i + 2, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day, self.perturbative_max_length, 1)
            # new_individual.showTree()
            self.individuals.append(new_individual)


        for i in range(0, int(self.num_individuals / 2)):
            #Full
            new_individual = Chromosome(self.seed, self.max_depth, self.max_depth - i + 2, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day, self.perturbative_max_length, 0)
            # new_individual.showTree()
            self.individuals.append(new_individual)

class Chromosome:
    def __init__(self, seed, max_depth, depth, problems, rooms, courses, days, curricula, num_rooms, periods_per_day, perturbative_max_length = 10, choice = 0, copy = False, tree = None):
        self.max_depth = max_depth
        self.depth = depth
        self.seed = seed
        self.problems = problems
        self.rooms = rooms
        self.courses = courses
        self.days = days
        self.curricula = curricula
        self.num_rooms = num_rooms
        self.periods_per_day = periods_per_day
        self.choice = choice
        if copy == False:
            self.createTree(choice)
        else:
            self.tree = tree.copy()
        self.evaluator = Evaluator(self.seed, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day)
        self.perturbative_max_length = perturbative_max_length
        
    def copy(self):
        copy = Chromosome(self.seed, self.max_depth, self.depth, self.problems, self.rooms, self.courses, self.days, self.curricula, self.num_rooms, self.periods_per_day, self.perturbative_max_length , self.choice, True, self.tree)
        copy.fitness = self.fitness
        return copy

    def evaluate(self):
        self.evaluator.evaluate(self.tree)
        self.fitness = self.evaluator.calculateFitness()
        print("fitness: " + str(self.fitness))

    def createTree(self, choice = 0):
        if choice == 0:
            # print("full")
            self.tree = Tree(self.seed)
            self.tree.createFull()
        else:
            # print("grow")
            self.tree = Tree(self.seed)
            self.tree.createGrow()
            
    def crossover(self, parent2):
        self.tree.crossover(parent2)
            
    def showTree(self):
        print("\n")
        print("--------- show tree ---------")
        self.tree.showTree(self.tree.root)


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
        # implement proper copy @TODO
        new_tree.depth = 0
        new_tree.max_depth = self.max_depth
        new_tree.root = self.copyHelper(self.root)
        # print('\n\n TREE CHILDREN')
        # print(new_tree.root.children)
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
            self.depth = level
            if type == 0:
                return self.returnTerminalNode()
            else:
                return self.returnTerminalNode(1)
        elif level == 0: #root
            functional_node = self.returnFuntionalNode()
            num_children = 2 if functional_node.id == 0 else random.randint(2, 3)
            if functional_node.id == 1:
                for i in range(0, num_children):
                    functional_node.children.append(self.full(level + 1))
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
                for i in range(0, num_children):
                    functional_node.children.append(self.full(level + 1))
            else:
                functional_node.children.append(self.full(level + 1, 0))
                functional_node.children.append(self.full(level + 1, 1))
            functional_node.num_children = num_children
            return functional_node

    
    def grow(self, level = 0, type = 0):
        if level == self.max_depth: #end here
            self.depth = level
            if type == 0:
                return self.returnTerminalNode()
            else:
                return self.returnTerminalNode(1)
        elif level == 0: #root
            self.root = self.full(level + 1)
            return self.root
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

    def showTree(self, node = None, level = 0):
      
        if node == None:
            pass
        elif level == 0:
            # at root
            print(self.root.description)  
               
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
        # print(" ======================== BEFORE =================================")
        # self.showTree(self.root)
        # print('\n\n')
        # parent2.showTree()
        # print('point1')
        # print(point1.description)
        # print('point2')
        # print(point2.description)
        point1_copy = self.copyHelper(point1)
        point2_copy = self.copyHelper(point2)

        point1 = point2_copy
        point2 = point1_copy
        # print('point1')
        # print(point1.description)
        # print('point2')
        # print(point2.description)
        # print(" ======================== AFTER!!!! =================================")
        # self.showTree(self.root)
        # print('\n\n')
        # parent2.showTree()

    def mutate(self):
        point = self.findCrossoverPoint()

    def mutateHelper(self, node, level = 0):
        if level > self.max_depth:
            pass

    def findCrossoverPoint(self, type = -1):
        
        place = random.randint(0, self.depth)
        point = self.findCrossPointHelper(self.root, place, type)
        return point

    def findMutatePoint(self):
        place = random.randint(0, self.depth)
        point = self.findMutatePointHelper(self.root, place)["node"]
        return point

    def findMutatePointHelper(self, node, depth, level = 0):
        if level == depth: #end
            return {
                "node": node,
                "level": level
            }
        else:
            place = random.randint(0, node.num_children - 1)
            if node.children[place].terminal == False:
                return self.findMutatePointHelper(node.children[place], depth, level + 1)
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
                place = random.randint(0, node.num_children - 1)
                if node.children[place].terminal == False:
                    return self.findCrossPointHelper(node.children[place], depth, type, level + 1)
                else:
                    return node
        else:
            if node.id == type:
                return node

            node = None
            for i in range(0, node.num_children):
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


    


