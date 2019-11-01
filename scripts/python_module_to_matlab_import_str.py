#!/usr/bin/python

# SYNTAX: python python_module_to_matlab_import_str.py PYTHON_MODULE_NAME

# Converts a python module (.py) into a string ready to be imported into a
# matlab environment. (Useful to 'convert' a .py into a .mat)

# NOTE: Supports int, float and str only!


import sys

module_name = sys.argv[1]
supported_types = [int, str, float]  # TODO: add list


# import the module
module = __import__(module_name)
# filter variables
var_names = dir(module)
# filter by name (exclude private and built-in varibales)
var_names = [n for n in var_names if n[0] != "_"]
# filter by type (supported types only)
var_names = [
    n for n in var_names if type(getattr(module, n)) in supported_types
]
# generate import string
matlab_import_str = ""
for n in var_names:
    value = getattr(module, n)
    if type(value) == str:
        value_str = "'" + value + "'"
    else:
        value_str = str(value)
    matlab_import_str += " " + n + " = " + value_str + ";"

# output matlab import string
sys.stdout.write(matlab_import_str)
