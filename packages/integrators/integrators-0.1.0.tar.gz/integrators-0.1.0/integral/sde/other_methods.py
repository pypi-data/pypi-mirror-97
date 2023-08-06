# -*- coding: utf-8 -*-

from integral import backend
from integral import profile


__all__ = [
    'exponential_euler',
]


def exponential_euler(func):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def int_f(y0, t, *args):
        f, linear_part, g = func(y0, t, *args)
        dW = backend.normal(0., 1., backend.shape(y0))
        dg = dt_sqrt * g * dW
        exp = backend.exp(linear_part * dt)
        y1 = y0 + (exp - 1) / linear_part * f + exp * dg
        return y1

    return int_f
