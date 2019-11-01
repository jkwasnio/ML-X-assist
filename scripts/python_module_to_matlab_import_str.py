#!/usr/bin/python

# SYNTAX: python python_module_to_matlab_import_str.py PYTHON_MODULE_NAME

# Converts a python module (.py) into a string ready to be imported into a
# matlab environment. (Useful to 'convert' a .py into a .mat)

# NOTE: Supports int, float and str only!


import sys
import numpy as np

module_name = sys.argv[1]

# define conversion from object to string by type
converter = {}

# shortcut for conversion
def convert(x):
    s = converter[type(x)](x)
    if s is None:
        return "'FAILED IMPORT'"
    return s


# register converters
converter[int] = lambda i: str(i)
converter[np.int8] = lambda i: str(i)
converter[np.int16] = lambda i: str(i)
converter[np.int32] = lambda i: str(i)
converter[np.int64] = lambda i: str(i)
converter[float] = lambda f: str(f)
converter[np.float16] = lambda f: str(f)
converter[np.float32] = lambda f: str(f)
converter[np.float64] = lambda f: str(f)
converter[np.complex] = lambda z: str(z)
converter[np.complex64] = lambda z: str(z)
converter[np.complex128] = lambda z: str(z)
converter[str] = lambda s: "'" + str(s) + "'"
converter[list] = lambda l: "[" + " ".join([convert(e) for e in l]) + "]"


def convert_np_nd_array(a):
    if len(a.shape) > 2:
        return  # unsupported
    # columns must be separated by spaces
    separator = ";"
    # coefficients must be separated by spaces
    if len(a.shape) == 1:
        separator = " "
    return "[" + separator.join([convert(e) for e in a]) + "]"


converter[np.ndarray] = convert_np_nd_array
# TODO: extend
supported_types = converter.keys()

# import the module
module = __import__(module_name)
# list attributes to be forwarded
attribute_names = dir(module)
# filter by name (exclude private and built-in varibales)
attribute_names = [n for n in attribute_names if n[0] != "_"]
# filter by type (supported types only)
attribute_names = [
    n for n in attribute_names if type(getattr(module, n)) in supported_types
]
# generate import string
matlab_import_str = ""
for n in attribute_names:
    value = getattr(module, n)
    value_str = convert(value)
    matlab_import_str += n + " = " + value_str + ";"

# output matlab import string
sys.stdout.write(matlab_import_str)
