'''
Created on Mar 29, 2011

Defines classes for generating operator and terminal instances, combines them 
to form population individuals, and provides means for evaluating individuals
to string representations and calculated values.

@author: erik
'''

import random
import definitions

# Global definitions of operators:
#('name', arity, 'input_type', 'output_type', function or 'function', 'symbol')
OPERATORS = [
('add', 2, 'num', 'num', definitions.add, '+'),
('subtract', 2, 'num', 'num', definitions.subtract, '-'),
('multiply', 2, 'num', 'num', definitions.multiply, '*'),
('divide', 2, 'num', 'num', definitions.divide, '/')
# An example of how an operator might be defined with a lambda function.
#('add', 2, 'num', 'num', lambda (a, b): a + b, '+'),
]

class InvalidParameterError(ValueError):
    """ The parameter is invalid. """
    pass

class OperatorInitError(Exception):
    """ Operator initialization failed. """
    pass

class Operator:
    """ Class describing an operator.
    
    The definition must be a tuple of the form ('name', arity, 'argument type',
    'return type', lambda function, and 'str_value').
    
    @param definition: The definition of an Operator. Must be a tuple of form
    ('name', arity, 'input_type', 'output_type',
    function or 'function', 'symbol')
    
    """
    def __init__(self, definition):
        self.name, self.arity, self.argument_type, \
        self.return_type, self.function, self.str_value = definition
        
        if isinstance(self.function, str):
            self.function = "func = " + self.function
            try:
                func = None
                exec self.function
                self.function = func
            except:
                raise OperatorInitError
        
    def __call__(self, *args):
        return self.function(*args)
    
    def __str__(self):
        return self.str_value
    
class Terminal:
    """ Class describing a terminal."""
    def __init__(self, value, is_var):
        self.is_var = is_var
        self.value = value
        self.str_value = str(self.value)
    
    def __str__(self):
        return self.str_value
    

class Individual:
    """ Define a data structure for GP solutions.
    
    @param variables: A list of the variable terminal instances used in
    generating the individual.
    
    """
    def __init__(self, variables):
        self.root = None
        self.branches = []
        self.vars = variables
        self.var_to_val = {}
        # Max depth of the tree of which this is the root.
        self.max_depth = None
        
    def __call__(self, values):
#        print "passed 'values'", values
        if not isinstance(values, list):
            print 'Parameter must be a list.'
            raise TypeError
        if not len(values) == len(self.vars):
            print 'Invalid parameter length. Value required for all variables.'
            raise ValueError
        
        self.var_to_val = dict(zip(self.vars, values))
        
        return self.evaluate(values)
           
    def __str__(self):
        return self.expression()
    
    def evaluate(self, values):
        """ Evaluate the value of the individual.
                
        @param values: list containing the values of the variables in the order
        the variables were created.       
        @return: The value of the individual.
        
        """
        
        # Base case.
        if isinstance(self.root, Terminal):
            if self.root.is_var:
                return self.var_to_val[self.root]
            else:
                return self.root.value
        # Recursive case.
        else:
            arguments = []
            for branch in self.branches:
                arguments.append(branch(values))
            arguments = tuple(arguments)
            try:
                return self.root(arguments)
            except (ArithmeticError, TypeError):
                raise
                
    def expression(self):
        """ Generate the expression representing the individual.
        
        @return: An expression representing the individual.
        
        """
        if not self.branches:
            return self.root.str_value
        else:
            str_list = [self.root.str_value]
            for child in self.branches:
                str_list.append(child.expression())
            return "(" + " ".join(str_list) + ")"
    

class Population:
    """ A class for initializing and storing a population of Individuals.
    
    As currently implemented population creation is accomplished thus:
    1) Create a Population instance
    2) Run make_operators(), make_vars(), and make_constants()
    3) Run populate()
    
    """
    def __init__(self):
        self.individuals = None
        self.operators = None
        self.vars = []
        self.constants = []
        self.terminals = []
        
    def make_operators(self):
        """ Generate operators. """
        self.operators = []
        for definition in OPERATORS:
            try:
                self.operators.append(Operator(definition))
            except OperatorInitError:
                raise
            
    def make_vars(self, *args):
        """ Generate variable terminals.
        
        @param args: Names of variable terminals to be created.
        
        """
        self.vars = []
        for var in args:
            self.vars.append(Terminal(var, True))
            
    def make_constants(self, low=-5, high=5, num=3):
        """ Generate constant terminals.
        
        @param low: Lower limit of random constants generated.
        @param high: Upper limit of random constants generated.
        @param num: Number of random constants to be generated.
        
        """
        self.constants = []
        for dummy in xrange(num):
            self.constants.append(Terminal(random.uniform(low, high), False))
            
    def make_individual(self, depth, kind):
        """ Generate an individual.
        
        @param depth: Tree depth for the individual.
        @param kind: Tree type for individual: 'full' or 'grow'
        @return: A tree representing an individual.
         
        """
        global kinds;
        kinds = ["full", "grow"]
        if not (depth >= 0 and kind in kinds):
            raise InvalidParameterError
        self.terminals = []
        self.terminals.extend(self.vars)
        self.terminals.extend(self.constants)
        indiv = Individual(self.vars)
        if kind == "full":
            indiv.max_depth = depth
            if depth == 0:
                indiv.root = random.choice(self.terminals)
            else:
                indiv.root = random.choice(self.operators)
                for dummy in range(indiv.root.arity):
                    indiv.branches.append(self.make_individual(depth - 1, kind))
            return indiv
        else:
            indiv.max_depth = depth
            if depth == 0:
                indiv.root = random.choice(self.terminals)
            else:
                ops_and_terms = self.terminals + self.operators
                
                indiv.root = random.choice(ops_and_terms)
                if not isinstance(indiv.root, Terminal):
                    for dummy in range(indiv.root.arity):
                        indiv.branches.append(self.make_individual(depth - 1, 
                                                                   kind))
            return indiv

    def populate(self, size, depth, kind="full"):
        """ Create a population of individuals.
        
        @param size: Size of the population
        @param depth: Tree depth for the individual.
        @param kind: Tree type for individual.
        
        """
        self.individuals = []
        if not size > 0:
#            print "populate(" + size + " " + depth + ", " + kind + ")"
            raise InvalidParameterError
        for dummy in range(size):
            self.individuals.append(self.make_individual(depth, kind))

#def main():
#    """ Testing the module. """
#    
#    import time
#    import copy
#    
#    # Test adding a new operator manually.
#    # Caution: mod leads to a lot of divide by zero errors
#    # in large individuals.
#    print "Adding an operator manually."
#    mod = ('mod', 2, 'num', 'num', lambda (a, b): a % b, '%')
#    OPERATORS.append(mod)
#    
#    # Setup a population of one to compare recursive and manual expressions.
#    print "Setting up a population instance."
#    pop = Population()
#    pop.make_operators()
#    pop.make_constants()
#    pop.make_vars('x')
#    
#    # Make a population of one.
#    print "Populating a small shallow population."
#    pop.populate(2, 2)
#    
#    # Check string representation of expressions.
#    i1 = pop.individuals[0]
#    print "Recursive representation of an expression:"
#    print i1
#    print "Manual representation of same expression:"
#    print i1.root
#    for branch1 in i1.branches:
#        print branch1.root
#        for branch2 in branch1.branches:
#            print branch2.root
#            
#    # Testing addition of max_depth field.
#    print 'Recursively, values of max_depth'        
#    print i1.max_depth
#    for branch1 in i1.branches:
#        print branch1.max_depth
#        for branch2 in branch1.branches:
#            print branch2.max_depth
#            
#    # Check evaluation of expression
#    print "testing evaluation:"
#    print i1, "evaluates to", i1([10])
#    
#    # Figuring out copying individuals        
#    i1copy = copy.deepcopy(i1)
#    print "i1:", i1
#    print "i1copy:", i1copy
#    print "i1 == i1copy:", i1 is i1copy
#    i1.branches.pop()
#    print "i1:", i1
#    print "i1copy:", i1copy
#    print "i1 == i1copy:", i1 is i1copy
#    
#
#    # Test population generation, and individual evaluation times.
#    print ""
#    print "Populating a larger deeper population."
#    time_taken = time.time() 
#    pop.populate(10, 10)
#    print "Population consists of", len(pop.individuals), "individuals."
#    time_taken = time.time() - time_taken
#    print 'Population generation time:', time_taken, "seconds"
#    print ""
#    i1 = pop.individuals[0]
#    time_taken = time.time() 
#    print i1, "evaluates to", i1([1])
#    time_taken = time.time() - time_taken
#    print 'Individual call time:', time_taken, "seconds"
#    
#    returns = []
#    for dummy in range(-10, 10):
#        returns.append(i1([dummy]))
#    print len(returns), returns
#
#if __name__ == "__main__":
#    main()   
