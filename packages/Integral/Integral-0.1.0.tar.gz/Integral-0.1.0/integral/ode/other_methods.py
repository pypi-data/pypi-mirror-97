# -*- coding: utf-8 -*-

from integral import profile
from integral import backend

__all__ = [
    'exponential_euler',
]


def exponential_euler(func, *args):
    dt = profile.get_dt()

    def int_f(x, t, *args):
        df, linear_part = func(x, t, *args)
        y = x + (backend.exp(linear_part * dt) - 1) / linear_part * df
        return y

    return int_f
