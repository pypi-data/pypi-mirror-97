# -*- coding: utf-8 -*-

from dynamics import profile
from dynamics import backend

__all__ = [
    'exponential_euler',
]


def exponential_euler(func, *args):
    dt = profile.get_dt()

    def int_f(y0, t, *args):
        df, linear_part = func(y0, t, *args)
        y = y0 + (backend.exp(linear_part * dt) - 1) / linear_part * df
        return y

    return int_f
