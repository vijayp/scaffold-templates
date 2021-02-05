#!/usr/bin/env ____PYTHON_VERSION
# Copyright (c) ____AUTHOR ____YEAR
# Autogenerated by ____GENERATOR_STRING

''' This is the python file that contains functions and most code for ____PROGRAM '''

import logging
from numbers import Number

def _check_number(n):
    if not isinstance(n, Number):
        raise TypeError('Only numbers are supported')

def add(lval, rval):
    ''' this adds the two numbers and returns the sum '''
    _check_number(lval)
    _check_number(rval)
    logging.debug('add is adding %lf to %lf ' % (lval, rval))
    return lval + rval

def sub(lval, rval):
    ''' this subtracts the two numbers and returns the difference '''
    _check_number(lval)
    _check_number(rval)
    logging.debug('add is subtracting %lf from %lf ' % (rval, lval))
    return lval - rval