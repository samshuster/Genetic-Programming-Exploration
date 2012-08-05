'''
Created on Apr 24, 2011

@author: erik
'''

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math
import time


class Animation:
    """ Class for animating a microGP experiment.
    
    An Animation instance is initialized with a microGP experiment instance.
    When called the instance plots the target function, and then successively
    plots the best match from each generation.
    
    """
    
    def __init__(self, experiment):
        plt.ion()
        self.target = experiment.target_func
        self.domain = experiment.fitness_accuracy
        self.populations = experiment.populations
        self.pdf_out = None
        
    def __call__(self):
        best = []
        for population in self.populations:
            best.append(population[0])
        
        plot_file = "plot_" + time.strftime('%Y_%m_%d_%H_%M_%S')
        try:
            self.pdf_out = PdfPages(plot_file + '.pdf')
        except IOError:
            print 'Could not create PDF file. File may be open'
        y_values = []
        
        for x in self.domain:
            y_values.append(eval(self.target))
        line, = plt.plot(self.domain, y_values, label = "Target")
        plt.legend()
        plt.draw()
        
        gen_count = 0
        line, = plt.plot(self.domain, self.domain)
        for candidate in best:
            gen_count = gen_count + 1
            y_values = []
            fitness = candidate[0]
            function = candidate[1]
            for x in self.domain:
                y_values.append(function([x]))
            line.set_ydata(y_values)
            line.set_label('Fitness: %.5f' % (fitness))
            plt.legend(loc=8, ncol=2, mode='expand')


            plt.title('Generation %i' % gen_count)
            plt.draw()
            
            if self.pdf_out:
                try:
                    self.pdf_out.savefig()
                except IOError:
                    print 'Could not save to PDF file. File may be open.'
        plt.show()    
        if self.pdf_out:
            try:
                self.pdf_out.close()
            except IOError:
                print 'Could not close PDF file.'
