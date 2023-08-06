# -*- coding: utf-8 -*-

import math
from integral import backend
from integral import profile

__all__ = [
    'euler',
    'heun',
    'milstein_Ito',
    'milstein_Stra',
]


def euler(f=None, g=None, scalar_wiener=None):
    """

    This method has have strong orders :math:`(p_d, p_s) = (1.0, 0.5)`.

    """
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def scalar_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args)[0] * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            dgdW = dg * dW
            return x + dfdt + dgdW

        return int_func

    def vector_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args) * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            dgdt = backend.sum(dg * dW, axis=-1)
            return x + dfdt + dgdt

        return int_func

    if (scalar_wiener is None) and (f is None) and (g is None):
        raise ValueError('Must provide "f" or "g" or "scalar" setting.')

    # scalar Wiener process #
    # --------------------- #
    elif (scalar_wiener is True) or (scalar_wiener is None):
        if f is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda f: scalar_wrapper(f, g)

        elif g is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda g: scalar_wrapper(f, g)

        else:
            assert f is not None
            assert g is not None
            return scalar_wrapper(f, g)

    # vector Wiener process #
    # --------------------- #
    else:
        if f is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda f: vector_wrapper(f, g)

        elif g is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda g: vector_wrapper(f, g)

        else:
            return vector_wrapper(f, g)


def heun(f=None, g=None, scalar_wiener=None):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def scalar_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args) * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            y_bar = x + dg * dW
            dg_bar = f_df(y_bar, t, *args)
            dgdW = 0.5 * (dg + dg_bar) * dW
            y = x + dfdt + dgdW
            return y

        return int_func

    def vector_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args) * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            y_bar = x + backend.sum(dg * dW, axis=-1)
            dg_bar = f_dg(y_bar, t, *args)
            dgdW = 0.5 * backend.sum((dg + dg_bar) * dW, axis=-1)
            return x + dfdt + dgdW

        return int_func

    if (scalar_wiener is None) and (f is None) and (g is None):
        raise ValueError('Must provide "f" or "g" or "scalar" setting.')

    # scalar Wiener process #
    # --------------------- #
    elif (scalar_wiener is True) or (scalar_wiener is None):
        if f is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda f: scalar_wrapper(f, g)

        elif g is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda g: scalar_wrapper(f, g)

        else:
            assert f is not None
            assert g is not None
            return scalar_wrapper(f, g)

    # vector Wiener process #
    # --------------------- #
    else:
        if f is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda f: vector_wrapper(f, g)

        elif g is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda g: vector_wrapper(f, g)

        else:
            return vector_wrapper(f, g)


def milstein_Ito(f=None, g=None, scalar_wiener=None):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def scalar_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            df = f_df(x, t, *args)
            dg = f_dg(x, t, *args)
            dfdt = df * dt
            dW = backend.normal(0., 1., backend.shape(dg))
            dgdW = dg * dW * dt_sqrt
            df_bar = x + dfdt + dg * dt_sqrt
            dg_bar = f_dg(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt - dt_sqrt)
            return x + dfdt + dgdW + extra_term

        return int_func

    def vector_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            df = f_df(x, t, *args)
            dg = backend.sum(f_dg(x, t, *args), axis=-1)
            dW = backend.normal(0., 1., backend.shape(dg))
            dfdt = df * dt
            df_bar = x + dfdt + backend.sum(dg * dt_sqrt, axis=-1)
            dg_bar = f_dg(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt - dt_sqrt)
            dgdW = dg * dW * dt_sqrt
            return x + dfdt + backend.sum(dgdW + extra_term, axis=-1)

        return int_func

    if (scalar_wiener is None) and (f is None) and (g is None):
        raise ValueError('Must provide "f" or "g" or "scalar" setting.')

    # scalar Wiener process #
    # --------------------- #
    elif (scalar_wiener is True) or (scalar_wiener is None):
        if f is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda f: scalar_wrapper(f, g)

        elif g is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda g: scalar_wrapper(f, g)

        else:
            assert f is not None
            assert g is not None
            return scalar_wrapper(f, g)

    # vector Wiener process #
    # --------------------- #
    else:
        if f is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda f: vector_wrapper(f, g)

        elif g is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda g: vector_wrapper(f, g)

        else:
            return vector_wrapper(f, g)


def milstein_Stra(f=None, g=None, scalar_wiener=None):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def scalar_wrapper(f, g):
        def int_func(y0, t, *args):
            df = f(y0, t, *args)
            dg = g(y0, t, *args)
            dW = backend.normal(0., 1., backend.shape(dg))
            dfdt = df * dt
            dgdW = dg * dW * dt_sqrt
            df_bar = y0 + dfdt + dg * dt_sqrt
            dg_bar = g(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt)
            return y0 + dfdt + dgdW + extra_term

        return int_func

    def vector_wrapper(f, g):
        def int_func(y0, t, *args):
            df = f(y0, t, *args)
            dg = backend.sum(g(y0, t, *args), axis=-1)
            dW = backend.normal(0., 1., backend.shape(dg))
            dfdt = df * dt
            dgdW = dg * dW * dt_sqrt
            df_bar = y0 + dfdt + backend.sum(dg * dt_sqrt, axis=-1)
            dg_bar = g(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt)
            return y0 + dfdt + backend.sum(dgdW + extra_term, axis=-1)

        return int_func

    if (scalar_wiener is None) and (f is None) and (g is None):
        raise ValueError('Must provide "f" or "g" or "scalar" setting.')

    # scalar Wiener process #
    # --------------------- #
    elif (scalar_wiener is True) or (scalar_wiener is None):
        if f is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda f: scalar_wrapper(f, g)

        elif g is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda g: scalar_wrapper(f, g)

        else:
            assert f is not None
            assert g is not None
            return scalar_wrapper(f, g)

    # vector Wiener process #
    # --------------------- #
    else:
        if f is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda f: vector_wrapper(f, g)

        elif g is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda g: vector_wrapper(f, g)

        else:
            return vector_wrapper(f, g)


def srk1w2_strong(f=None, g=None, iterations_num=30):
    """Order 1.0 strong SRK methods for SDEs with multi-dimensional Wiener process.

    The Butcher table is:

    .. math::

        \\begin{array}{c|ccc|ccc|ccc|}
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            \\hline 0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 1 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & -1 & 0 & 0 & & \\\\
            \\hline & 1 & 0 & 0 & 1 & 0 & 0 & 0 & 1 / 2 & -1 / 2
        \\end{array}

    References
    ----------

    [1] Rößler, Andreas. "Strong and weak approximation methods for stochastic differential
        equations—some recent developments." Recent developments in applied probability and
        statistics. Physica-Verlag HD, 2010. 127-153.
    [2] Rößler, Andreas. "Runge–Kutta methods for the strong approximation of solutions of
        stochastic differential equations." SIAM Journal on Numerical Analysis 48.3
        (2010): 922-952.

    """
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    B1_21 = 1.
    B1_31 = -1.
    alpha_1 = 1.
    beta1_1 = 1.
    beta2_2 = 0.5
    beta2_3 = -0.5

    def wrapper(f, g):
        def int_func(x, t, *args):
            g_t_X1s1 = g(x, t, *args)
            noise_shape = backend.shape(g_t_X1s1)
            dim = backend.shape(g_t_X1s1)[-1]

            # single Ito integrals #
            # -------------------- #
            I1 = backend.normal(0., dt_sqrt, noise_shape)

            # double Ito integrals #
            # -------------------- #
            I2 = backend.zeros(shape=(dim + 1, dim + 1))
            # I^{00}(h_n)
            I2[0, 0] = 0.5 * dt ** 2

            #  I^{alpha,0}(h_n), alpha = 1, 2, …, m
            ζ = backend.normal(0., dt_sqrt, noise_shape)
            I2[1:, 0] = 0.5 * dt * (I1 + ζ / 3.0 ** 0.5)

            #  I^{0,alpha}(h_n), alpha = 1, 2, …, m
            ζ = backend.normal(0, dt_sqrt, noise_shape)
            I2[0, 1:] = 0.5 * dt * (I1 - ζ / 3.0 ** 0.5)

            # I^{alpha,beta}(h_n), alpha,beta = 1, 2, …, m
            I = backend.eye(dim)
            h = (2.0 / dt) ** 0.5
            A = backend.zeros(shape=(dim, dim))
            for k in range(1, iterations_num + 1):
                X = backend.normal(loc=0.0, scale=1.0, size=dim)
                Y = backend.normal(loc=0.0, scale=1.0, size=dim) + h * I1
                A += (backend.outer(X, Y) - backend.outer(Y, X)) / k
            I2[1:, 1:] = 0.5 * (backend.outer(I1, I1) - dt * I) + 0.5 * dt * A / math.pi

            # numerical integration #
            # --------------------- #
            f_t_X0s1 = f(t, x, *args)
            g_t_X2s1 = g_t_X1s1

            X1s2 = x + B1_21 * g_t_X1s1[:, 0] * I2[1, 1] / dt_sqrt + \
                   B1_21 * g_t_X2s1[:, 1] * I2[2, 1] / dt_sqrt
            X2s2 = x + B1_21 * g_t_X1s1[:, 0] * I2[1, 2] / dt_sqrt + \
                   B1_21 * g_t_X2s1[:, 1] * I2[2, 2] / dt_sqrt
            g_t_X1s2 = g(X1s2, t, *args)
            g_t_X2s2 = g(X2s2, t, *args)

            X1s3 = x + B1_31 * g_t_X1s1[:, 0] * I2[1, 1] / dt_sqrt + \
                   B1_31 * g_t_X2s1[:, 1] * I2[2, 1] / dt_sqrt
            X2s3 = x + B1_31 * g_t_X1s1[:, 0] * I2[1, 2] / dt_sqrt + \
                   B1_31 * g_t_X2s1[:, 1] * I2[2, 2] / dt_sqrt
            g_t_X1s3 = g(X1s3, t, *args)
            g_t_X2s3 = g(X2s3, t, *args)

            X1 = beta1_1 * I1[0] * g_t_X1s1[:, 0] + \
                 beta2_2 * dt_sqrt * g_t_X1s2[:, 0] + \
                 beta2_3 * dt_sqrt * g_t_X1s3[:, 0]
            X2 = beta1_1 * I1[1] * g_t_X2s1[:, 1] + \
                 beta2_2 * dt_sqrt * g_t_X2s2[:, 1] + \
                 beta2_3 * dt_sqrt * g_t_X2s3[:, 1]
            y = x + h * alpha_1 * f_t_X0s1 + X1 + X2
            return y

        return int_func
