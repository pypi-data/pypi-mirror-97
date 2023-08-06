# -*- coding: utf-8 -*-

import numpy as np
from numba.extending import overload

standard_normal = np.random.standard_normal
shape = np.shape
sum = np.sum
mean = np.mean
any = np.any
exp = np.exp
