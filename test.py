'''
Created on Apr 17, 2011

@author: erik
'''

#import numpy as np
#import matplotlib.pyplot as plt
#import structures as struct
#import random
#import experiment
#
## Initialize a Population
#pop = struct.Population()
#pop.make_operators()
#pop.make_constants()
#pop.make_vars('x')
#
## Populate population, select an individual to work with
#pop.populate(1, 5)
#i = pop.individuals[0]
# Print the individual and it's values over a domain
#print i
#for n in range(-10, 10):
#    print i([n])
# Plot an individuals values over a domain
#y = []
#x = np.arange(0, 10, .1)
#for n in x:
#    y.append(i([n]))
#    
#plt.plot(x, y)
#plt.show()


## Trying random node selection
#pop.populate(1, 5, 'full')
#i = pop.individuals[0]
#subtree = None
#n = 1
#def traverse(tree):
#    global n
#    global subtree
#    if not tree.branches:
#        r = random.uniform(0, 1)
#        if r < (1.0 / n):
#            subtree = tree
#        n = n + 1
#        return
#    else:
#        for branch in tree.branches:
#            traverse(branch)
#        r = random.uniform(0, 1)
#        if r < (1.0 / n):
#            subtree = tree
#        n = n + 1
#        return        
#
#traverse(i)
#print i
#print subtree

#e = experiment.Experiment(pop_size = 100, num_generations = 100, max_depth = 3)   