# -*- coding: utf-8 -*-


from integral import backend
from integral import profile

__all__ = [
    'srk1w1_scalar',
    'srk2w1_scalar',
    'KlPl_scalar',
]


def srk1w1_scalar(f=None, g=None):
    """Order 1.5 Strong SRK Methods for SDEs witdt Scalar Noise.

    This method has have strong orders :math:`(p_d, p_s) = (2.0,1.5)`.

    The Butcher table is:

    .. math::

        \\begin{array}{l|llll|llll|llll}
            0   &&&&&  &&&&  &&&& \\\\
            3/4 &3/4&&&& 3/2&&& &&&& \\\\
            0   &0&0&0&& 0&0&0&& &&&&\\\\
            \\hline
            0 \\\\
            1/4 & 1/4&&& & 1/2&&&\\\\
            1 & 1&0&&& -1&0&\\\\
            1/4& 0&0&1/4&&  -5&3&1/2\\\\
            \\hline
            & 1/3& 2/3& 0 & 0 & -1 & 4/3 & 2/3&0 & -1 &4/3 &-1/3 &0 \\\\
            \\hline
            & &&&& 2 &-4/3 & -2/3 & 0 & -2 & 5/3 & -2/3 & 1
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

    A0_21 = 0.75
    A1_21 = 0.25
    B0_21 = 1.5
    B1_21 = 0.5
    A1_31 = 1
    B1_31 = -1
    A1_43 = 0.25
    B1_41 = -5
    B1_42 = 3
    B1_43 = 0.5
    alpha1 = 1 / 3
    alpha2 = 2 / 3
    c0_2 = 0.75
    c1_2 = 0.25
    c1_3 = 1
    c1_4 = 0.25
    beta1_1 = -1
    beta1_2 = 4 / 3
    beta1_3 = 2 / 3
    beta2_1 = -1
    beta2_2 = 4 / 3
    beta2_3 = -1 / 3
    beta3_1 = 2
    beta3_2 = -4 / 3
    beta3_3 = -2 / 3
    beta4_1 = -2
    beta4_2 = 5 / 3
    beta4_3 = -2 / 3
    beta4_4 = 1

    def wrapper(f_df, f_dg):
        def init_func(x, t, *args):
            I1 = backend.normal(0.0, dt_sqrt, backend.shape(x))
            I0 = backend.normal(0.0, dt_sqrt, backend.shape(x))
            I10 = 0.5 * dt * (I1 + I0 / 3.0 ** 0.5)
            I11 = 0.5 * (I1 ** 2 - dt)
            I111 = (I1 ** 3 - 3 * dt * I1) / 6

            H0s1 = x
            H1s1 = x
            f_t_H0s1 = f_df(t, H0s1, *args)
            g_t_H1s1 = f_dg(t, H1s1, *args)

            H0s2 = x + dt * A0_21 * f_t_H0s1 + B0_21 * g_t_H1s1 * I10 / dt
            H1s2 = x + dt * A1_21 * f_t_H0s1 + dt_sqrt * B1_21 * g_t_H1s1
            f_t_H0s2 = f_df(t + c0_2 * dt, H0s2, *args)
            g_t_H1s2 = f_dg(t + c1_2 * dt, H1s2, *args)

            H0s3 = x
            H1s3 = x + dt * (A1_31 * f_t_H0s1) + dt_sqrt * B1_31 * g_t_H1s1
            g_t_H1s3 = f_dg(t + c1_3 * dt, H1s3, *args)

            H1s4 = x + dt * A1_43 * f_df(t, H0s3, *args) + \
                   dt_sqrt * (B1_41 * g_t_H1s1 + B1_42 * g_t_H1s2 + B1_43 * g_t_H1s3)
            g_t_H1s4 = f_dg(t + c1_4 * dt, H1s4, *args)

            y1 = x + dt * (alpha1 * f_t_H0s1 + alpha2 * f_t_H0s2) + \
                 (beta1_1 * I1 + beta2_1 * I11 / dt_sqrt + beta3_1 * I10 / dt + beta4_1 * I111 / dt) * g_t_H1s1 + \
                 (beta1_2 * I1 + beta2_2 * I11 / dt_sqrt + beta3_2 * I10 / dt + beta4_2 * I111 / dt) * g_t_H1s2 + \
                 (beta1_3 * I1 + beta2_3 * I11 / dt_sqrt + beta3_3 * I10 / dt + beta4_3 * I111 / dt) * g_t_H1s3 + \
                 (beta4_4 * I111 / dt) * g_t_H1s4
            return y1

        return init_func

    if f is not None and g is not None:
        return wrapper(f, g)

    elif f is not None:
        return lambda g: wrapper(f, g)

    elif g is not None:
        return lambda f: wrapper(f, g)

    else:
        raise ValueError('Must provide "f" or "g".')


def srk2w1_scalar(f=None, g=None):
    """Order 1.5 Strong SRK Methods for SDEs witdt Scalar Noise.

    This method has have strong orders :math:`(p_d, p_s) = (3.0,1.5)`.

    The Butcher table is:

    .. math::

        \\begin{array}{c|cccc|cccc|ccc|}
            0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & & & & \\\\
            1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & & & & \\\\
            1 / 2 & 1 / 4 & 1 / 4 & 0 & 0 & 1 & 1 / 2 & 0 & 0 & & & & \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & & & & \\\\
            \\hline 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & & & & \\\\
            1 / 4 & 1 / 4 & 0 & 0 & 0 & -1 / 2 & 0 & 0 & 0 & & & & \\\\
            1 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & & & & \\\\
            1 / 4 & 0 & 0 & 1 / 4 & 0 & 2 & -1 & 1 / 2 & 0 & & & & \\\\
            \\hline & 1 / 6 & 1 / 6 & 2 / 3 & 0 & -1 & 4 / 3 & 2 / 3 & 0 & -1 & -4 / 3 & 1 / 3 & 0 \\\\
            \\hline & & & & &2 & -4 / 3 & -2 / 3 & 0 & -2 & 5 / 3 & -2 / 3 & 1
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

    A0_21 = 1
    A0_31 = 0.25
    A0_32 = 0.25
    A1_21 = 0.25
    A1_31 = 1
    A1_43 = 0.25
    B0_31 = 1
    B0_32 = 0.5
    B1_21 = -0.5
    B1_31 = 1
    B1_41 = 2
    B1_42 = -1
    B1_43 = 0.5
    alpha1 = 1 / 6
    alpha2 = 1 / 6
    alpha3 = 2 / 3
    c0_2 = 1
    c0_3 = 0.5
    c1_2 = 0.25
    c1_3 = 1
    c1_4 = 0.25
    beta1_1 = -1
    beta1_2 = 4 / 3
    beta1_3 = 2 / 3
    beta2_1 = 1
    beta2_2 = -4 / 3
    beta2_3 = 1 / 3
    beta3_1 = 2
    beta3_2 = -4 / 3
    beta3_3 = -2 / 3
    beta4_1 = -2
    beta4_2 = 5 / 3
    beta4_3 = -2 / 3
    beta4_4 = 1

    def wrapper(f_df, f_dg):
        def init_func(x, t, *args):
            I1 = backend.normal(0.0, dt_sqrt, backend.shape(x))
            I0 = backend.normal(0.0, dt_sqrt, backend.shape(x))
            I10 = 0.5 * dt * (I1 + I0 / 3.0 ** 0.5)
            I11 = 0.5 * (I1 ** 2 - dt)
            I111 = (I1 ** 3 - 3 * dt * I1) / 6

            H0s1 = x
            H1s1 = x
            f_t_H0s1 = f_df(t, H0s1, *args)
            g_t_H1s1 = f_dg(t, H1s1, *args)

            H0s2 = x + dt * (A0_21 * f_t_H0s1)
            H1s2 = x + dt * (A1_21 * f_t_H0s1) + dt_sqrt * (B1_21 * g_t_H1s1)
            f_t_H0s2 = f_df(t + c0_2 * dt, H0s2, *args)
            g_t_H1s2 = f_dg(t + c1_2 * dt, H1s2, *args)

            H0s3 = x + dt * (A0_31 * f_t_H0s1 + A0_32 * f_t_H0s2) + \
                   (B0_31 * g_t_H1s1 + B0_32 * g_t_H1s2) * I10 / dt
            H1s3 = x + dt * (A1_31 * f_t_H0s1) + dt_sqrt * (B1_31 * g_t_H1s1)
            f_t_H0s3 = f_dg(t + c0_3 * dt, H0s3, *args)
            g_t_H1s3 = f_dg(t + c1_3 * dt, H1s3, *args)

            H1s4 = x + dt * (A1_43 * f_t_H0s3) + \
                   dt_sqrt * (B1_41 * g_t_H1s1 + B1_42 * g_t_H1s2 + B1_43 * g_t_H1s3)
            g_t_H1s4 = f_dg(t + c1_4 * dt, H1s4, *args)

            y1 = x + dt * (alpha1 * f_t_H0s1 + alpha2 * f_t_H0s2 + alpha3 * f_t_H0s3) + \
                 (beta1_1 * I1 + beta2_1 * I11 / dt_sqrt + beta3_1 * I10 / dt + beta4_1 * I111 / dt) * g_t_H1s1 + \
                 (beta1_2 * I1 + beta2_2 * I11 / dt_sqrt + beta3_2 * I10 / dt + beta4_2 * I111 / dt) * g_t_H1s2 + \
                 (beta1_3 * I1 + beta2_3 * I11 / dt_sqrt + beta3_3 * I10 / dt + beta4_3 * I111 / dt) * g_t_H1s3 + \
                 (beta4_4 * I111 / dt) * g_t_H1s4

            return y1

        return init_func

    if f is not None and g is not None:
        return wrapper(f, g)

    elif f is not None:
        return lambda g: wrapper(f, g)

    elif g is not None:
        return lambda f: wrapper(f, g)

    else:
        raise ValueError('Must provide "f" or "g".')


def KlPl_scalar(f=None, g=None):
    """Order 1.0 Strong SRK Methods for SDEs witdt Scalar Noise.

    This method has have orders :math:`p_s = 1.0`.

    The Butcher table is:

    .. math::

        \\begin{array}{c|cc|cc|cc|c}
            0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 0 & & \\\\
            \\hline 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 1 & 0 & 1 & 0 & & \\\\
            \\hline 0 & 1 & 0 & 1 & 0 & -1 & 1 \\\\
            \\hline & & & 1 & 0 & 0 & 0
        \\end{array}

    References
    ----------

    [1] P. E. Kloeden, E. Platen, Numerical Solution of Stochastic Differential
        Equations, 2nd Edition, Springer, Berlin Heidelberg New York, 1995.
    """
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    A1_21 = 1
    B1_21 = 1
    alpha_1 = 1
    beta1_1 = 1
    beta2_1 = -1
    beta2_2 = 1
    beta3_1 = 1

    def wrapper(f_df, g_dg):
        def init_func(x, t0, *args):
            I1 = backend.normal(0.0, dt_sqrt, backend.shape(x))
            I0 = backend.normal(0.0, dt_sqrt, backend.shape(x))
            I10 = 0.5 * dt * (I1 + I0 / 3.0 ** 0.5)
            I11 = 0.5 * (I1 ** 2 - dt)

            X0_1 = x
            X1_1 = x
            f_t_H0s1 = f_df(t0, X0_1, *args)
            g_t_H1s1 = g_dg(t0, X1_1, *args)

            X1_2 = x + dt * A1_21 * f_t_H0s1 + dt_sqrt * B1_21 * g_t_H1s1
            g_t_H1s2 = g_dg(t0, X1_2, *args)

            y1 = x + dt * alpha_1 * f_t_H0s1 + \
                 (beta1_1 * I1 + beta2_1 * I11 / dt_sqrt + beta3_1 * I10 / dt) * g_t_H1s1 + \
                 beta2_2 * I11 / dt_sqrt * g_t_H1s2
            return y1

        return init_func

    if f is not None and g is not None:
        return wrapper(f, g)

    elif f is not None:
        return lambda g: wrapper(f, g)

    elif g is not None:
        return lambda f: wrapper(f, g)

    else:
        raise ValueError('Must provide "f" or "g".')
