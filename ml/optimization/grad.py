# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/710_optimization.grad.ipynb (unless otherwise specified).

__all__ = ['naive_grad']

# Cell
import numpy as np

def naive_grad(f):
    '''
    CENTRAL FINITE DIFFERENCE CALCULATION
    '''
    def _grad(x):
        h = np.cbrt(np.finfo(float).eps)
        d = len(x)
        nabla = np.zeros(d)
        for i in range(d):
            x_for = np.copy(x)
            x_back = np.copy(x)
            x_for[i] += h
            x_back[i] -= h
            nabla[i] = (f(x_for) - f(x_back))/(2*h)
        return nabla

    return _grad