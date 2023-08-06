# -*- coding: utf-8 -*-


import numpy as np
from numba.extending import overload

__all__ = [
    # basic operations
    'standard_normal',
    'shape',
    'exp',

    # methods
    'set_ops',
    'set_backend',
]

_backend = 'numpy'  # default backend is NumPy

standard_normal = np.random.standard_normal
shape = np.shape
exp = np.exp


def set_ops(**kwargs):
    if 'standard_normal' in kwargs:
        global standard_normal
        standard_normal = kwargs.pop('standard_normal')

    if 'shape' in kwargs:
        global shape
        shape = kwargs.pop('shape')

    if 'exp' in kwargs:
        global exp
        exp = kwargs.pop('exp')

    if len(kwargs) > 0:
        raise ValueError(f"Unknown operators: {list(kwargs.keys())}")


@overload(np.random.standard_normal)
def standard_normal_func(size):
    if len(size) == 0:
        def standard_normal(size):
            return np.random.normal(0., 1.)
    else:
        def standard_normal(size):
            return np.random.normal(0., 1., size)

    return standard_normal


def set_backend(backend):
    global _backend
    _backend = backend

    if backend == 'numpy':
        set_ops(standard_normal=np.random.standard_normal,
                shape=np.shape,
                exp=np.exp)

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
