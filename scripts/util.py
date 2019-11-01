import numpy as np


def discrete_eval(f, xs):
    res = np.zeros(len(xs))
    for i in range(len(xs)):
        res[i] = f(xs[i])
    return res
