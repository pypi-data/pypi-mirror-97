# -*- coding: utf-8 -*-

"""
Implementation of the paper:

- Wang, Zhen. "A numerical method for delayed fractional-order
  differential equations." Journal of Applied Mathematics 2013.

"""

import math
import numpy as np
import matplotlib.pyplot as plt

alpha = 0.95
m = int(np.ceil(alpha))
dt = 0.01
delay_tau = 0.8



def f_before_t0(t):
    return 19.


def f(y, y_delay, t):
    return 3.5 * y * (1 - y_delay / 19)


def a(j, n):
    if j == 0:
        return n ** (alpha + 1) - (n - alpha) * (n + 1) ** alpha
    else:
        exponent = alpha + 1
        return (n - j + 2) ** exponent + (n - j) ** exponent - 2 * (n - j + 1) ** exponent


def b(j, n):
    return dt ** alpha / alpha * ((n - j + 1) ** alpha - (n - j) ** alpha)


times = np.arange(0, 100, dt)

hist_f = []
hist_val = [0.]
hist_delay = []


y = 0.
yp = 0.
for n, t in enumerate(times):
    n += 1

    # get delay var
    if t < delay_tau:
        y_delay = f_before_t0(t - delay_tau)
    else:
        m = int(np.ceil(delay_tau / dt))
        delta = m - delay_tau / dt
        if m == 1:
            y_delay = delta * yp + (1 - delta) * hist_val[-1]
        else:
            y_delay = delta * hist_val[-m] + (1 - delta) * hist_val[-m + 1]
    hist_delay.append(y_delay)

    # get f value
    fv = f(y, y_delay, t)
    hist_f.append(fv)

    # get yp
    yp = 0
    for j in range(0, n):
        yp += b(j, n) * hist_f[j]
    yp /= math.gamma(alpha)
    for k in range(0, m):
        yp += f_before_t0(k) * t ** k / math.factorial(k)

    # get delay var
    if t < delay_tau:
        y_delay = f_before_t0(t - delay_tau)
    else:
        m = int(np.ceil(delay_tau / dt))
        delta = m - delay_tau / dt
        if m == 1:
            y_delay = delta * yp + (1 - delta) * hist_val[-1]
        else:
            y_delay = delta * hist_val[-m] + (1 - delta) * hist_val[-m + 1]

    # get y
    y = yp + dt ** alpha / math.gamma(alpha + 2) * f(yp, y_delay, t)

    hist_val.append(y)


plt.plot(hist_val)
plt.show()

