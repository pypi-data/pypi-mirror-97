# -*- coding: utf-8 -*-


import numpy as np
from numba.extending import overload

__all__ = [
    # basic operations
    'normal',
    'shape',
    'exp',

    # methods
    'set_ops',
    'set_backend',
]

_backend = 'numpy'  # default backend is NumPy

normal = np.random.normal
shape = np.shape
exp = np.exp
sum = np.sum
zeros = np.zeros
ones = np.ones
eye = np.eye
outer = np.outer


def set_ops(**kwargs):
    if 'normal' in kwargs:
        global normal
        normal = kwargs.pop('normal')

    if 'shape' in kwargs:
        global shape
        shape = kwargs.pop('shape')

    if 'exp' in kwargs:
        global exp
        exp = kwargs.pop('exp')

    if 'sum' in kwargs:
        global sum
        sum = kwargs.pop('sum')

    if 'ones' in kwargs:
        global ones
        ones = kwargs.pop('ones')

    if 'zeros' in kwargs:
        global zeros
        zeros = kwargs.pop('zeros')

    if 'eye' in kwargs:
        global eye
        eye = kwargs.pop('eye')

    if 'outer' in kwargs:
        global outer
        outer = kwargs.pop('outer')

    if len(kwargs) > 0:
        raise ValueError(f"Unknown operators: {list(kwargs.keys())}")


@overload(np.random.normal)
def normal_func(loc, scale, size):
    if len(size) == 0:
        def normal(loc, scale, size):
            return loc + scale * np.random.standard_normal()
    else:
        def normal(loc, scale, size):
            return loc + scale * np.random.standard_normal(size)

    return normal


def set_backend(backend):
    global _backend
    _backend = backend

    if backend == 'numpy':
        set_ops(normal=np.random.normal,
                shape=np.shape,
                exp=np.exp,
                sum=np.sum)

    elif backend == 'numba-gpu':
        pass

    elif backend == 'pytorch':
        pass

    elif backend == 'tensorflow':
        pass

    elif backend == 'jax':
        pass

    else:
        raise ValueError(f'Unknown backend: {backend}.')
