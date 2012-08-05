Instructions for MicroGP!
************************
Set Basic Experiment Parameters:
These control the most rudimentary options of your microgp experiment. 
POPULATION SIZE: is an integer greater than 6 and describes the size of the population. 
NUMBER OF GENERATIONS: is an integer greater than 0 which describes how many generations your experiment will last for before it fails automatically.
MAX DEPTH OF TREE: is an integer greater than 0 which describes how high the Abstract Syntax Tree describing your individual is.
 The larger the number, the more complex the functions that individuals hold will be.
TREE TYPE: Full tree is a full binary tree, while a grow tree does not have to be full. Both, however, will vary in size through generations.

Set Reproduction Rates:
These control how often certain procedures are done on your individuals.
MUTATION RATE: The percentage of time that an individual is mutated, meaning that a node of
 its function tree is chosen at random and then changed to a completely new random tree.
CROSSOVER RATE: The percentage of time that an individual is paired with another individual to 
undergo crossover, which means that two randomly selected nodes of their respective trees will be swapped.
CLONING RATE: The percentage of time that an individual is passed through without being modified.
ELITISM NUMBER: A number between 0 and the population size,
which describes how many of the best individuals automatically get passed onto the next generation

Set Constant Range for Individuals:
These represent the constant values that individuals will randomly select from

Set Fitness Parameters:
The Testing values represent the range in which the fitness function will calculae an individuals fitness, 
while the increment will determine how precise and how many measurements you want to be taken. The fitness success cutoff is a
 number greater than 0 and less than or equal to 1, which represents how fit an individual has to be for the experiment to end in success.

Target Function:
The target function that individuals are trying to emulate.
NOTE: Any complex mathematical function needs to be proceeded by math and written in python syntax. e.g. sin(x) would be written as:
math.sin(x) and x^2 would be written as:
math.pow(x,2)
Also, only x can be used as a variable!