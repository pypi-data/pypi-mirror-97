# -*- coding: utf-8 -*-

"""
https://en.wikipedia.org/wiki/List_of_Runge%E2%80%93Kutta_methods
https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
"""

from integral import profile

__all__ = [
    'rkf45',
    'rkdp',
    'ck',
    'bs',
]


def rkf45(f=None, epsilon=None, adaptive=None):
    """The Runge–Kutta–Fehlberg method for ordinary differential equations.

    The method presented in Fehlberg's 1969 paper has been dubbed the
    RKF45 method, and is a method of order :math:`O(h^4)` with an error
    estimator of order :math:`O(h^5)`. The novelty of Fehlberg's method is
    that it is an embedded method from the Runge–Kutta family, meaning that
    identical function evaluations are used in conjunction with each other
    to create methods of varying order and similar error constants.

    It has the characteristics of:

        - method stage = 6
        - method order = 5
        - Butcher Tables:

    .. math::

        \\begin{array}{l|lllll}
            0 & & & & & & \\\\
            1 / 4 & 1 / 4 & & & & \\\\
            3 / 8 & 3 / 32 & 9 / 32 & & \\\\
            12 / 13 & 1932 / 2197 & -7200 / 2197 & 7296 / 2197 & \\\\
            1 & 439 / 216 & -8 & 3680 / 513 & -845 / 4104 & & \\\\
            1 / 2 & -8 / 27 & 2 & -3544 / 2565 & 1859 / 4104 & -11 / 40 & \\\\
            \\hline & 16 / 135 & 0 & 6656 / 12825 & 28561 / 56430 & -9 / 50 & 2 / 55 \\\\
            & 25 / 216 & 0 & 1408 / 2565 & 2197 / 4104 & -1 / 5 & 0
        \\end{array}

    References
    ----------

    [1] https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta%E2%80%93Fehlberg_method
    [2] Erwin Fehlberg (1969). Low-order classical Runge-Kutta formulas with step
        size control and their application to some heat transfer problems . NASA
        Technical Report 315.
        https://ntrs.nasa.gov/api/citations/19690021375/downloads/19690021375.pdf

    """

    def wrapper_without_adaptive(f):
        def int_func(x, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 4, t + dt / 4, *args)
            k3 = f(x + dt * k1 * 3 / 32 + dt * k2 * 9 / 32, t + dt * 3 / 8, *args)
            k4 = f(x + dt * k1 * 1932 / 2197 - dt * k2 * 7200 / 2197 +
                   dt * k3 * 7296 / 2197, t + dt * 12 / 13,
                   *args)
            k5 = f(x + dt * k1 * 439 / 216 - dt * k2 * 8 + dt * k3 * 3680 / 513 -
                   dt * k4 * 845 / 4104, t + dt,
                   *args)
            k6 = f(x - dt * k1 * 8 / 27 + dt * k2 * 2 - dt * k3 * 3544 / 2565 +
                   dt * k4 * 1859 / 4104 - dt * k5 * 11 / 40, t + dt / 2, *args)
            y_new = x + dt * (k1 * 16 / 135 + k3 * 6656 / 12825 + k4 * 28561 / 56430 -
                              k5 * 9 / 50 + k6 * 2 / 55)
            return y_new

        return int_func

    def wrapper_with_adaptive(f, epsilon):
        def int_func(x, dt, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 4, t + dt / 4, *args)
            k3 = f(x + dt * k1 * 3 / 32 + dt * k2 * 9 / 32, t + dt * 3 / 8, *args)
            k4 = f(x + dt * k1 * 1932 / 2197 - dt * k2 * 7200 / 2197 +
                   dt * k3 * 7296 / 2197, t + dt * 12 / 13, *args)
            k5 = f(x + dt * k1 * 439 / 216 - dt * k2 * 8 + dt * k3 * 3680 / 513 -
                   dt * k4 * 845 / 4104, t + dt, *args)
            k6 = f(x - dt * k1 * 8 / 27 + dt * k2 * 2 - dt * k3 * 3544 / 2565 +
                   dt * k4 * 1859 / 4104 - dt * k5 * 11 / 40, t + dt / 2, *args)
            y_new = x + dt * (k1 * 16 / 135 + k3 * 6656 / 12825 +
                              k4 * 28561 / 56430 - k5 * 9 / 50 + k6 * 2 / 55)
            error = sum(abs(25 / 216 * k1 + 1408 / 2565 * k3 + 2197 / 4104 * k4 - k5 / 5))
            if error > epsilon:
                h_new = 0.9 * dt * (epsilon / error) ** 0.2
            else:
                h_new = dt
            return y_new, h_new

        return int_func

    if (adaptive is None) or (not adaptive):
        dt = profile.get_dt()

        if f is None:
            return lambda f: wrapper_without_adaptive(f)
        else:
            return wrapper_without_adaptive(f)

    else:
        assert f is None
        epsilon = 0.1 if epsilon is None else epsilon

        if f is None:
            return lambda f: wrapper_with_adaptive(f, epsilon)
        else:
            return wrapper_with_adaptive(f, epsilon)


def rkdp(f=None, epsilon=None, adaptive=None):
    """The Dormand–Prince method for ordinary differential equations.

    The DOPRI method, is an explicit method for solving ordinary differential equations
    (Dormand & Prince 1980). The Dormand–Prince method has seven stages, but it uses only
    six function evaluations per step because it has the FSAL (First Same As Last) property:
    the last stage is evaluated at the same point as the first stage of the next step.
    Dormand and Prince chose the coefficients of their method to minimize the error of
    the fifth-order solution. This is the main difference with the Fehlberg method, which
    was constructed so that the fourth-order solution has a small error. For this reason,
    the Dormand–Prince method is more suitable when the higher-order solution is used to
    continue the integration, a practice known as local extrapolation
    (Shampine 1986; Hairer, Nørsett & Wanner 2008, pp. 178–179).

    It has the characteristics of:

        - method stage = 7
        - method order = 5
        - Butcher Tables:

    .. math::

        \\begin{array}{l|llllll}
            0 & \multicolumn{4}{|l} {} \\\\
            1 / 5 & 1 / 5 & & & \\\\
            3 / 10 & 3 / 40 & 9 / 40 & & & \\\\
            4 / 5 & 44 / 45 & -56 / 15 & 32 / 9 & & \\\\
            8 / 9 & 19372 / 6561 & -25360 / 2187 & 64448 / 6561 & -212 / 729 & \\\\
            1 & 9017 / 3168 & -355 / 33 & 46732 / 5247 & 49 / 176 & -5103 / 18656 & \\\\
            1 & 35 / 384 & 0 & 500 / 1113 & 125 / 192 & -2187 / 6784 & 11 / 84 & \\\\
            \\hline & 35 / 384 & 0 & 500 / 1113 & 125 / 192 & -2187 / 6784 & 11 / 84 & 0 \\\\
            & 5179 / 57600 & 0 & 7571 / 16695 & 393 / 640 & -92097 / 339200 & 187 / 2100 & 1 / 40
        \\end{array}

    References
    ----------

    [1] https://en.wikipedia.org/wiki/Dormand%E2%80%93Prince_method
    [2] Dormand, J. R.; Prince, P. J. (1980), "A family of embedded Runge-Kutta formulae",
        Journal of Computational and Applied Mathematics, 6 (1): 19–26,
        doi:10.1016/0771-050X(80)90013-3.
    """

    def wrapper_without_adaptive(f):
        def int_func(x, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 5, t + dt / 5, *args)
            k3 = f(x + dt * k1 * 3 / 40 + dt * k2 * 9 / 40, t + dt * 3 / 10, *args)
            k4 = f(x + dt * k1 * 44 / 45 - dt * k2 * 56 / 15 + dt * k3 * 32 / 9,
                   t + dt * 4 / 5, *args)
            k5 = f(x + dt * k1 * 19372 / 6561 - dt * k2 * 25360 / 2187 +
                   dt * k3 * 64448 / 6561 - dt * k4 * 212 / 729,
                   t + dt * 8 / 9, *args)
            k6 = f(x + dt * k1 * 9017 / 3168 - dt * k2 * 355 / 33 + dt * k3 * 46732 / 5247 +
                   dt * k4 * 49 / 176 - dt * k5 * 5103 / 18656, t + dt, *args)
            y_new = x + dt * (k1 * 35 / 384 + k3 * 500 / 1113 + k4 * 125 / 192 -
                              k5 * 2187 / 6784 + k6 * 11 / 84)
            return y_new

        return int_func

    def wrapper_with_adaptive(f, epsilon):
        def int_func(x, dt, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 5, t + dt / 5, *args)
            k3 = f(x + dt * k1 * 3 / 40 + dt * k2 * 9 / 40, t + dt * 3 / 10, *args)
            k4 = f(x + dt * k1 * 44 / 45 - dt * k2 * 56 / 15 + dt * k3 * 32 / 9,
                   t + dt * 4 / 5, *args)
            k5 = f(x + dt * k1 * 19372 / 6561 - dt * k2 * 25360 / 2187 +
                   dt * k3 * 64448 / 6561 - dt * k4 * 212 / 729,
                   t + dt * 8 / 9, *args)
            k6 = f(x + dt * k1 * 9017 / 3168 - dt * k2 * 355 / 33 + dt * k3 * 46732 / 5247 +
                   dt * k4 * 49 / 176 - dt * k5 * 5103 / 18656, t + dt, *args)
            k7 = f(x + dt * k1 * 35 / 384 + dt * k3 * 500 / 1113 +
                   dt * k4 * 125 / 192 - dt * k5 * 2187 / 6784 + dt * k6 * 11 / 84,
                   t + dt, *args)
            y_new = x + dt * (k1 * 35 / 384 + k3 * 500 / 1113 + k4 * 125 / 192 -
                              k5 * 2187 / 6784 + k6 * 11 / 84)
            error = sum(abs(5179 / 57600 * k1 + 7571 / 16695 * k3 + 393 / 640 * k4 -
                            k5 * 92097 / 339200 + k6 * 187 / 2100 + k7 / 40))
            if error > epsilon:
                h_new = 0.9 * dt * (epsilon / error) ** 0.2
            else:
                h_new = dt
            return y_new, h_new

        return int_func

    if (adaptive is None) or (not adaptive):
        dt = profile.get_dt()

        if f is None:
            return lambda f: wrapper_without_adaptive(f)
        else:
            return wrapper_without_adaptive(f)

    else:
        assert f is None
        epsilon = 0.1 if epsilon is None else epsilon

        if f is None:
            return lambda f: wrapper_with_adaptive(f, epsilon)
        else:
            return wrapper_with_adaptive(f, epsilon)


def ck(f=None, epsilon=None, adaptive=None):
    """The Cash–Karp method  for ordinary differential equations.

    The Cash–Karp method was proposed by Professor Jeff R. Cash from Imperial College London
    and Alan H. Karp from IBM Scientific Center. it uses six function evaluations to calculate
    fourth- and fifth-order accurate solutions. The difference between these solutions is then
    taken to be the error of the (fourth order) solution. This error estimate is very convenient
    for adaptive stepsize integration algorithms.

    It has the characteristics of:

        - method stage = 6
        - method order = 4
        - Butcher Tables:

    .. math::

        \\begin{array}{l|lllll}
            0 & & & & & & \\\\
            1 / 5 & 1 / 5 & & & & & \\\\
            3 / 10 & 3 / 40 & 9 / 40 & & & \\\\
            3 / 5 & 3 / 10 & -9 / 10 & 6 / 5 & & \\\\
            1 & -11 / 54 & 5 / 2 & -70 / 27 & 35 / 27 & & \\\\
            7 / 8 & 1631 / 55296 & 175 / 512 & 575 / 13824 & 44275 / 110592 & 253 / 4096 & \\\\
            \\hline & 37 / 378 & 0 & 250 / 621 & 125 / 594 & 0 & 512 / 1771 \\\\
            & 2825 / 27648 & 0 & 18575 / 48384 & 13525 / 55296 & 277 / 14336 & 1 / 4
        \\end{array}

    References
    ----------

    [1] https://en.wikipedia.org/wiki/Cash%E2%80%93Karp_method
    [2] J. R. Cash, A. H. Karp. "A variable order Runge-Kutta method for initial value
        problems with rapidly varying right-hand sides", ACM Transactions on Mathematical
        Software 16: 201-222, 1990. doi:10.1145/79505.79507
    """

    def wrapper_without_adaptive(f):

        def int_func(x, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 5, t + dt / 5, *args)
            k3 = f(x + dt * k1 * 3 / 40 + dt * k2 * 9 / 40, t + dt * 3 / 10, *args)
            k4 = f(x + dt * k1 * 3 / 10 - dt * k2 * 9 / 10 + dt * k3 * 6 / 5,
                   t + dt * 3 / 5, *args)
            k5 = f(x - dt * k1 * 11 / 54 + dt * k2 * 5 / 2 - dt * k3 * 70 / 27 +
                   dt * k4 * 35 / 27, t + dt, *args)
            k6 = f(x + dt * k1 * 1631 / 55296 + dt * k2 * 175 / 512 + dt * k3 * 575 / 13824 +
                   dt * k4 * 44275 / 110592 + dt * k5 * 253 / 4096, t + dt * 7 / 8, *args)
            y_new = x + dt * (k1 * 37 / 378 + k3 * 250 / 621 + k4 * 125 / 594 + k6 * 512 / 1771)
            return y_new

        return int_func

    def wrapper_with_adaptive(f, epsilon):
        def int_func(x, dt, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 5, t + dt / 5, *args)
            k3 = f(x + dt * k1 * 3 / 40 + dt * k2 * 9 / 40, t + dt * 3 / 10, *args)
            k4 = f(x + dt * k1 * 3 / 10 - dt * k2 * 9 / 10 + dt * k3 * 6 / 5,
                   t + dt * 3 / 5, *args)
            k5 = f(x - dt * k1 * 11 / 54 + dt * k2 * 5 / 2 - dt * k3 * 70 / 27 +
                   dt * k4 * 35 / 27, t + dt, *args)
            k6 = f(x + dt * k1 * 1631 / 55296 + dt * k2 * 175 / 512 + dt * k3 * 575 / 13824 +
                   dt * k4 * 44275 / 110592 + dt * k5 * 253 / 4096, t + dt * 7 / 8, *args)
            y_new = x + dt * (k1 * 37 / 378 + k3 * 250 / 621 + k4 * 125 / 594 + k6 * 512 / 1771)
            error = sum(abs(2825 / 27648 * k1 + 18575 / 48384 * k3 +
                            13525 / 55296 * k4 + k5 * 277 / 14336 + k6 / 4))
            if error > epsilon:
                h_new = 0.9 * dt * (epsilon / error) ** 0.2
            else:
                h_new = dt
            return y_new, h_new

        return int_func

    if (adaptive is None) or (not adaptive):
        dt = profile.get_dt()

        if f is None:
            return lambda f: wrapper_without_adaptive(f)
        else:
            return wrapper_without_adaptive(f)

    else:
        assert f is None
        epsilon = 0.1 if epsilon is None else epsilon

        if f is None:
            return lambda f: wrapper_with_adaptive(f, epsilon)
        else:
            return wrapper_with_adaptive(f, epsilon)


def bs(f=None, epsilon=None, adaptive=None):
    """The Bogacki–Shampine method for ordinary differential equations.

    The Bogacki–Shampine method was proposed by Przemysław Bogacki and Lawrence F.
    Shampine in 1989 (Bogacki & Shampine 1989). The Bogacki–Shampine method is a
    Runge–Kutta method of order three with four stages with the First Same As Last
    (FSAL) property, so that it uses approximately three function evaluations per
    step. It has an embedded second-order method which can be used to implement adaptive step size.

    It has the characteristics of:

        - method stage = 4
        - method order = 3
        - Butcher Tables:

    .. math::

        \\begin{array}{l|lll}
            0 & & & \\\\
            1 / 2 & 1 / 2 & & \\\\
            3 / 4 & 0 & 3 / 4 & \\\\
            1 & 2 / 9 & 1 / 3 & 4 / 9 \\\\
            \\hline & 2 / 9 & 1 / 3 & 4 / 90 \\\\
            & 7 / 24 & 1 / 4 & 1 / 3 & 1 / 8
        \\end{array}

    References
    ----------

    [1] https://en.wikipedia.org/wiki/Bogacki%E2%80%93Shampine_method
    [2] Bogacki, Przemysław; Shampine, Lawrence F. (1989), "A 3(2) pair of Runge–Kutta
        formulas", Applied Mathematics Letters, 2 (4): 321–325, doi:10.1016/0893-9659(89)90079-7
    """

    def wrapper_without_adaptive(f):

        def int_func(x, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 2, t + dt / 2, *args)
            k3 = f(x + dt * k2 * 3 / 4, t + dt * 3 / 4, *args)
            y_new = x + dt * (k1 * 2 / 9 + k2 / 3 + k3 * 4 / 9)
            return y_new

        return int_func

    def wrapper_with_adaptive(f, epsilon):
        def int_func(x, dt, t, *args):
            k1 = f(x, t, *args)
            k2 = f(x + dt * k1 / 2, t + dt / 2, *args)
            k3 = f(x + dt * k2 * 3 / 4, t + dt * 3 / 4, *args)
            k4 = f(x + dt * k1 * 2 / 9 + dt * k2 / 3 + dt * k3 * 4 / 9, t + dt, *args)
            y_new = x + dt * (k1 * 2 / 9 + k2 / 3 + k3 * 4 / 9)
            error = sum(abs(7 / 24 * k1 + k2 / 4 + k3 / 3 + k4 / 8))
            if error > epsilon:
                h_new = 0.9 * dt * (epsilon / error) ** 0.2
            else:
                h_new = dt
            return y_new, h_new

        return int_func

    if (adaptive is None) or (not adaptive):
        dt = profile.get_dt()

        if f is None:
            return lambda f: wrapper_without_adaptive(f)
        else:
            return wrapper_without_adaptive(f)

    else:
        assert f is None
        epsilon = 0.1 if epsilon is None else epsilon

        if f is None:
            return lambda f: wrapper_with_adaptive(f, epsilon)
        else:
            return wrapper_with_adaptive(f, epsilon)


def DOP853(func=None, epsilon=None, adaptive=None):
    """The DOP853 method for ordinary differential equations.

    DOP853 is an explicit Runge-Kutta method of order 8(5,3) due to Dormand & Prince
    (with stepsize control and dense output).


    References
    ----------

    [1] E. Hairer, S.P. Norsett and G. Wanner, "Solving ordinary Differential Equations
        I. Nonstiff Problems", 2nd edition. Springer Series in Computational Mathematics,
        Springer-Verlag (1993).
    [2] http://www.unige.ch/~hairer/software.html
    """
    pass
