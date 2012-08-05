'''
Created on Apr 18, 2011

@author: erik
'''
#import math
#import numpy as np
#import matplotlib.pyplot as plt
#import structures
#
#pop = structures.Population()
#pop.make_operators()
#pop.make_constants(-2, 2, 2)
#pop.make_vars('x')
#pop.populate(1, 20)
#fitness = {}
#objective = 'x**2'
#domain = np.arange(-5, 5.1, .1)
#
##for ind in pop.individuals:
##    print ind
#
#for ind in pop.individuals:
#    whys = []
#    for x in domain:
#        diff = eval(objective) - ind([x])
#        norm_diff = abs(diff)
#        whys.append(norm_diff)
##    print whys
#    sum = 0
#    for y in whys:
#        sum += y
#    fitness[ind] = sum
#
#pairs = fitness.items()
#best_pair = pairs[0]
#for pair in pairs:
#    if pair[1] < best_pair[1]:
#        best_pair = pair
##print pairs
##print best_pair
#best_indiv = best_pair[0]
#
#y_obj = []
#y_exp = []
#for x in domain:
#    y_obj.append(eval(objective))
#    y_exp.append(best_indiv([x]))
#
#plt.plot(domain, y_obj, domain, y_exp)
#plt.show()