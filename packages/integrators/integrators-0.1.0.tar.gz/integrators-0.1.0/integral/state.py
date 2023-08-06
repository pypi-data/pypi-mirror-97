# -*- coding: utf-8 -*-

import numpy as np


class DiffEqState(object):
    def __init__(self, size, *args, monitors=None, **kwargs):
        self.data = {}
        self.mon = {}
        for arg in args:
            self.data[arg] = np.zeros(size)
        for k, w in kwargs.items():
            self.data[k] = np.ones(size) * w
        for k in monitors:
            self.mon[k] = []

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value


