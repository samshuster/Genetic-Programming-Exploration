'''
Created on Apr 16, 2011

Contains function definitions for Operators.

@author: erik
'''

#inf = float('inf')

def add(args):
    """ Add two numbers. """
    num1, num2 = args
    return num1 + num2

def subtract(args):
    """ Subtract second number from first. """
    num1, num2 = args
    return num1 - num2

def multiply(args):
    """ Multiply two numbers. """
    num1, num2 = args
    return num1 * num2

def divide(args):
    """ Safe divide returns 1 on divide by zero. """
    num1, num2 = args
    try:
        quotient = float(num1) / float(num2)
        return quotient
    except ZeroDivisionError:
        return 1
#        if a > 0:
#            return inf
#        elif a < 0:
#            return -inf
#        else:
#            return inf/inf
