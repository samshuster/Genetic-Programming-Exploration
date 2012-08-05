'''Created on March 30 @author Sam Shuster'''
import random
import math
import copy
import numpy as np
from animate import Animation

from greedy_selection import GreedySelection
import structures
from experiment_exceptions import InputError

FGENERATION = 1

class Experiment(object):
    '''Experiment Class'''


    def __init__(self):
        """ Make Experiment based on arbitrary keywords """
        self.pop_size = 50
        self.num_generations = 20
        self.s_method = GreedySelection()
        self.s_method_string = "greedy"
        self.max_depth = 3
        self.op_list = ['+', '-', '/', '*']
        self.vars = 'x'
        self.constant_max = 5
        self.constant_min = -5
        self.constant_num = int(math.pow(2, self.max_depth))
        #The rates must add up to 100!
        self.m_rate_const = 10
        self.c_rate_const = 80
        self.e_rate_const = 10
        self.m_rate = None
        self.c_rate = None
        self.e_rate = None
        self.elitism_num = int(math.ceil(0.05*self.pop_size))
        self.t_type = "full"
        #The function that will be attempted to be emulated:
        self.target_func = 'math.pow(x,2)'
        self.fitness_min = -2
        self.fitness_max = 2
        self.fitness_incr = 0.1
        self.fitness_accuracy = np.arange(-2, 2, 0.1)
        self.fitness_cutoff = 0.75
        #List for animation
        self.populations = []
        #Variables for tree traversal
        self.traverse_num = 1
        self.num = 1
        self.subtree = None
        self.m_subtree = None
        self.f_subtree = None

        
        
    def change_variable(self, **kwargs):
        """Changes an arbitrary parameter"""  
        for key in kwargs:
            if key == 'pop_size':
                self.pop_size = kwargs[key]
            if key == 'num_generations':
                self.num_generations = kwargs[key]
            if key == 's_method':
                self.s_method_string = kwargs[key]
            if key == 'max_depth':
                self.max_depth = kwargs[key]
            if key == 'm_rate':
                self.m_rate_const = kwargs[key]
            if key == 'c_rate':
                self.c_rate_const = kwargs[key]
            if key == 'e_rate':
                self.e_rate_const = kwargs[key]
            if key == 'elitism_num':
                self.elitism_num = kwargs[key]
            if key == 't_type':
                self.t_type = kwargs[key]
            if key == 'constant_max':
                self.constant_max = kwargs[key]
            if key == 'constant_min':
                self.constant_min = kwargs[key]
            if key == 'constant_num':
                self.constant_num = kwargs[key]
            if key == 'target_func':
                self.target_func = kwargs[key]
            if key == 'fitness_max':
                self.fitness_max = kwargs[key]
            if key == 'fitness_min':
                self.fitness_min = kwargs[key]
            if key == 'fitness_incr':
                self.fitness_incr = kwargs[key]
            
    def start(self):
        """ Start the experiment """
        self.check_input()
        self.standardize_rates()
        self.create_fitness_array()
        self.populations = []
        self.pop = structures.Population()
        self.pop.make_constants(self.constant_min, self.constant_max, 
                                self.constant_num)
        self.pop.make_vars(self.vars)
        self.pop.make_operators()
        self.pop.populate(self.pop_size, self.max_depth, self.t_type)
        self.run_experiment(FGENERATION, self.pop) 
    
    def check_input(self):
        """ Checks User Input"""
        try:
            self.pop_size = int(self.pop_size)
            self.num_generations = int(self.num_generations)
            self.max_depth = int(self.max_depth)
            self.c_rate_const = float(self.c_rate_const)
            self.e_rate_const = float(self.e_rate_const)
            self.m_rate_const = float(self.m_rate_const)
            self.elitism_num = int(self.elitism_num)
            self.constant_max = float(self.constant_max)
            self.constant_min = float(self.constant_min)
            self.constant_num = int(self.constant_num)
            self.fitness_max = float(self.fitness_max)
            self.fitness_min = float(self.fitness_min)
            self.fitness_incr = float(self.fitness_incr)
            self.fitness_cutoff = float(self.fitness_cutoff)
            
        except ValueError:
            raise InputError("Invalid Input", 
                             "Input was not valid. i.e. string for int")
        if self.pop_size <= 5:
            raise InputError("pop_size", "pop_size cannot be less than 6")
        if self.num_generations <= 0:
            raise InputError("num_generations",
                             "num_generations cannot be less than 1")
        if self.s_method is None:
            raise InputError("s_method",
                             "s_method does not exist!")
        if self.max_depth < 1:
            raise InputError("max_depth",
                             "max_depth cannot be less than 1")
        if self.constant_max < self.constant_min:
            raise InputError("constant_max and constant_min",
                             "constant_max must be >= than constant_min")
        if self.constant_num < 0:
            raise InputError("contant_num",
                             "contant_num must be >= 0")
        if self.m_rate_const < 0:
            raise InputError("m_rate",
                             "m_rate must be >= 0")
        if self.c_rate_const < 0:
            raise InputError("c_rate",
                             "c_rate must be >= 0")
        if self.e_rate_const < 0:
            raise InputError("e_rate",
                             "e_rate must be >= 0")
        if ((self.m_rate_const + self.c_rate_const + 
                  self.e_rate_const) != 100):
            raise InputError("all_rates",
                             "Reproduction Rates must add up to 100!")
        if self.elitism_num < 0 or self.elitism_num > self.pop_size:
            raise InputError("elitism_num",
                             "elitism_num must be >= 0 and <= pop_size")
        #Would be nice to access this from structures so its more adaptable
        if (not self.t_type == "grow" and not self.t_type == "full"):
            raise InputError("t_type",
                             self.t_type + " does not exist!")
        try:
            x = 1
            eval(self.target_func)
        except NameError:
            raise InputError("target_func",
                             "target_func is not valid!")
        if (self.fitness_min > self.fitness_max):
            raise InputError("fitness_min and fitness_max",
                             "fitness_max must be > fitness_min")  
        if (self.fitness_incr <= 0):
            raise InputError("fitness_incr",
                             "fitness_incr must be > 0")
        if (self.fitness_cutoff <=0 or self.fitness_cutoff > 1):
            raise InputError("fitness_cutoff",
                             "fitness_cutoff must be > 0 and <= 1")
        self.choose_selection_function()
        if (self.s_method is None):
            raise InputError("s_method",
                             "s_method is not valid!")
            
    def choose_selection_function(self):
        """ Chooses selection function based off of string """
        if self.s_method_string == "greedy":
            self.s_method = GreedySelection()
        else:
            self.s_method = GreedySelection()
        
    def create_fitness_array(self):
        """Creates fitness aray from the userdefined parameters"""
        self.fitness_accuracy = np.arange(self.fitness_min,
                                          self.fitness_max,
                                          self.fitness_incr)   
    def standardize_rates(self):
        """ Standardize the reproduction rates """
        self.m_rate = self.m_rate_const
        self.c_rate = self.c_rate_const
        self.e_rate = self.e_rate_const
        self.c_rate += self.m_rate 
        self.e_rate += self.c_rate
        
    def run_experiment(self, gen_num, population):
        """Run Experiment; a recursive function
        
        @param gen_num: The current generation number
        
        @param population: The current population
        
        """    
        next_gen = []
        ordered_fit_list = self.eval_ffunctions(population)
        
        self.populations.append(copy.deepcopy(ordered_fit_list))

        self.s_method.set_up(ordered_fit_list)
        for individual in xrange(self.elitism_num):
            next_gen.append(ordered_fit_list[individual][1])
        
        while (len(next_gen) < self.pop_size):
            breed_method_num = 100* random.random()
            if (breed_method_num < self.c_rate and self.pop_size - 
                len(next_gen) > 1):
                individual = self.s_method.select(2)
                individual = self.crossover(individual)
            elif breed_method_num < self.m_rate:
                individual = self.s_method.select(1)
                individual = self.mutate(individual)
            else:
                individual = self.s_method.select(1)
                
            for ind in individual:
                next_gen.append(ind)
                
                       
        population.individuals = next_gen
        print gen_num, ordered_fit_list
        if self.criterion_satisfied(ordered_fit_list):
            print gen_num
            print ordered_fit_list [0][0]
            print ordered_fit_list[0][1]
            animated = Animation(self)
            animated()

            #would be nice to store ordered_fit_list to other function
            #that would allow users to plot any of the individuals
            return ordered_fit_list[0][1]
        if gen_num >= self.num_generations:
            print "FAILED"
            print ordered_fit_list [0][0]
            print ordered_fit_list[0][1]
            animated = Animation(self)
            animated()
            return ordered_fit_list[0][1]
        gen_num += 1    
        self.run_experiment(gen_num, population)
    
    def criterion_satisfied(self, fit_list):
        '''Does current pop contain goal specimen?'''
        if fit_list[0][0] > self.fitness_cutoff:
            return True  
        
    
    
    def eval_ffunctions(self, current_pop):
        '''Evaluate Fitness User Specified Fitness Function
        @bug: only works for one variable at the moment
        @param current_pop: The current population, type Population
        @return: An ordered dictionary of fitness levels
        
        '''
        fitness_dict = {}
        for individual in current_pop.individuals:
            #print "New Individual",individual
            residual_sum = 0
            for input in self.fitness_accuracy:
                x = input
                theoretical = eval(self.target_func)
                experimental = individual([input])
                residual = math.pow((experimental - theoretical), 2)
                residual_sum += residual
            adjusted_fitness = residual_sum + 1
            adjusted_fitness = 1 / adjusted_fitness
            fitness_dict[adjusted_fitness] = individual
        fitness_list = sorted(fitness_dict.items(), reverse = True)
        return fitness_list
               
    def crossover(self, individuals):
        '''Crossover two different Parse-Trees with user defined constant
        @bug: will not handle any other trees than full
        @param individuals: The list of two individuals 
        
        @return: the list of two crossed-over individuals
        
        '''
        #print "old mother", individuals[0]
        #print "old father", individuals[1]
        mother = copy.deepcopy(individuals[0])
        father = copy.deepcopy(individuals[1])
        self.traverse(mother, True)  
        self.traverse_num = 1
        self.traverse(father, False)
        self.traverse_num = 1
        ftemp = copy.deepcopy(self.f_subtree)
        mtemp = copy.deepcopy(self.m_subtree)
        
        self.m_subtree.root = ftemp.root
        self.m_subtree.branches = ftemp.branches
        self.m_subtree.var_to_val = ftemp.var_to_val
        self.m_subtree.max_depth = ftemp.max_depth
        self.m_subtree.vars = ftemp.vars
        
        self.f_subtree.root = mtemp.root
        self.f_subtree.branches = mtemp.branches
        self.f_subtree.var_to_val = mtemp.var_to_val
        self.f_subtree.max_depth = mtemp.max_depth
        self.f_subtree.vars = mtemp.vars
        
        #print "mother ",mother
        #print "father ",father
        return [mother, father]
    
    def mutate(self, individual):
        '''Mutate part of the genome with user defined constant
        @bug: will not handle any trees other than full
        @param individual: The list of one individual
        
        @return: The list of one mutated individual
        '''
        ind = copy.deepcopy(individual[0])
        self.num = 1
        self.traverse(ind, True)
        branch_depth = random.randint(0, self.m_subtree.max_depth)
        
        temp = self.pop.make_individual(branch_depth, self.t_type)
        self.m_subtree.branches = temp.branches
        self.m_subtree.root = temp.root
        self.m_subtree.var_to_val = temp.var_to_val
        self.m_subtree.max_depth = temp.max_depth
        self.m_subtree.vars = temp.vars
        return [ind]
        
        
    def traverse(self, tree, is_mother):
        """Traverses a tree recursively """
        if not tree.branches:
            rand = random.uniform(0, 1)
            if rand < (1.0 / self.traverse_num):
                if (is_mother): 
                    self.m_subtree = tree
                    
                else:
                    self.f_subtree = tree
            self.traverse_num = self.traverse_num + 1
            return
        else:
            for branch in tree.branches:
                self.traverse(branch, is_mother)
            rand = random.uniform(0, 1)
            if rand < (1.0 / self.traverse_num):
                if (is_mother):
                    self.m_subtree = tree
                else:
                    self.f_subtree = tree
            self.traverse_num = self.traverse_num + 1
            return
        
