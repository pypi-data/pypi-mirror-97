# -*- coding: utf-8 -*-

"""
https://en.wikipedia.org/wiki/List_of_Runge%E2%80%93Kutta_methods#Kutta's_third-order_method
"""

from dynamics import profile


__all__ = [
    'euler',
    'midpoint',
    'heun2',
    'ralston2',
    'rk2',
    'rk3',
    'heun3',
    'ralston3',
    'ssprk3',
    'rk4',
    'ralston4',
    'rk4_38rule',
]


def euler(func, ):
    """The Euler method is first order. The lack of stability
    and accuracy limits its popularity mainly to use as a
    simple introductory example of a numeric solution method.

    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        return y0 + dt * func(y0, t, *args)

    return int_func


def midpoint(func, return_im=False):
    """midpoint method for ordinary differential equations.

    The (explicit) midpoint method is a second-order method
    with two stages.

    It has the characteristics of:

        - method stage = 2
        - method order = 2
        - Butcher Tables:

    .. math::

        \\begin{array}{c|cc}
            0 & 0 & 0 \\\\
            1 / 2 & 1 / 2 & 0 \\\\
            \\hline & 0 & 1
        \\end{array}

    """
    dt = profile.get_dt()

    if not return_im:
        def int_func(y0, t, *args):
            k1 = func(y0, t, *args)
            k2 = func(y0 + dt * k1 / 2, t + dt / 2, *args)
            y = y0 + dt * k2
            return y

    else:
        raise NotImplementedError

    return int_func


def heun2(func, return_im=False):
    """Heun's method for ordinary differential equations.

    Heun's method is a second-order method with two stages.
    It is also known as the explicit trapezoid rule, improved
    Euler's method, or modified Euler's method.

    It has the characteristics of:

        - method stage = 2
        - method order = 2
        - Butcher Tables:

    .. math::

        \\begin{array}{c|cc}
            0.0 & 0.0 & 0.0\\\\
            1.0 & 1.0 & 0.0\\\\
        \\hline & 0.5 & 0.5

    """
    dt = profile.get_dt()

    if not return_im:
        def int_func(y0, t, *args):
            k1 = func(y0, t, *args)
            k2 = func(y0 + dt * k1, t + dt, *args)
            y = y0 + dt * (k1 * 0.5 + k2 * 0.5)
            return y

    else:
        raise NotImplementedError

    return int_func


def ralston2(func, return_im=False):
    """Ralston's method for ordinary differential equations.

    Ralston's method is a second-order method with two stages and
    a minimum local error bound.

    It has the characteristics of:

        - method stage = 2
        - method order = 2
        - Butcher Tables:

    .. math::

        \\begin{array}{c|cc}
            0 & 0 & 0 \\\\
            2 / 3 & 2 / 3 & 0 \\\\
            \\hline & 1 / 4 & 3 / 4
        \\end{array}
    """
    dt = profile.get_dt()

    if not return_im:
        def int_func(y0, t, *args):
            k1 = func(y0, t, *args)
            k2 = func(y0 + dt * k1 * 2 / 3, t + dt * 2 / 3, *args)
            y = y0 + dt * (k1 / 4 + k2 * 3 / 4)
            return y

    else:
        raise NotImplementedError

    return int_func


def rk2(func, beta=2 / 3):
    """Runge–Kutta methods for ordinary differential equations.

    Generic second-order method.

    It has the characteristics of:

        - method stage = 2
        - method order = 2
        - Butcher Tables:

    .. math::

        \\begin{array}{c|cc}
            0 & 0 & 0 \\\\
            \\beta & \\beta & 0 \\\\
            \\hline & 1 - {1 \\over 2 * \\beta} & {1 \over 2 * \\beta}
        \\end{array}
    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + beta * dt * k1, t + beta * dt, *args)
        y = y0 + dt * ((1 - 1 / (2 * beta)) * k1 + 1 / (2 * beta) * k2)
        return y

    return int_func


def rk3(func, *args):
    """Classical third-order Runge-Kutta method for ordinary differential equations.

    It has the characteristics of:

        - method stage = 3
        - method order = 3
        - Butcher Tables:

    .. math::

        \\begin{array}{c|ccc}
            0 & 0 & 0 & 0 \\\\
            1 / 2 & 1 / 2 & 0 & 0 \\\\
            1 & -1 & 2 & 0 \\\\
            \\hline & 1 / 6 & 2 / 3 & 1 / 6
        \\end{array}

    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + dt / 2 * k1, t + dt / 2, *args)
        k3 = func(y0 - dt * k1 + 2 * dt * k2, t + dt, *args)
        return y0 + dt / 6 * (k1 + 4 * k2 + k3)

    return int_func


def heun3(func, return_im=False):
    """Heun's third-order method for ordinary differential equations.

    It has the characteristics of:

        - method stage = 3
        - method order = 3
        - Butcher Tables:

    .. math::

        \\begin{array}{c|ccc}
            0 & 0 & 0 & 0 \\\\
            1 / 3 & 1 / 3 & 0 & 0 \\\\
            2 / 3 & 0 & 2 / 3 & 0 \\\\
            \\hline & 1 / 4 & 0 & 3 / 4
        \\end{array}

    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + dt / 3 * k1, t + dt / 3, *args)
        k3 = func(y0 + 2 / 3 * dt * k2, t + dt * 2 / 3, *args)
        return y0 + dt / 4 * (k1 + 3 * k3)

    return int_func


def ralston3(func, return_im=False):
    """Ralston's third-order method for ordinary differential equations.

    It has the characteristics of:

        - method stage = 3
        - method order = 3
        - Butcher Tables:

    .. math::

        \\begin{array}{c|ccc}
            0 & 0 & 0 & 0 \\\\
            1 / 2 & 1 / 2 & 0 & 0 \\\\
            3 / 4 & 0 & 3 / 4 & 0 \\\\
            \\hline & 2 / 9 & 1 / 3 & 4 / 9
        \\end{array}

    References
    ----------

    [1] Ralston, Anthony (1962). "Runge-Kutta Methods with Minimum Error Bounds".
        Math. Comput. 16 (80): 431–437. doi:10.1090/S0025-5718-1962-0150954-0

    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + dt / 2 * k1, t + dt / 2, *args)
        k3 = func(y0 + 3 / 4 * dt * k2, t + dt * 3 / 4, *args)
        return y0 + dt / 9 * (2 * k1 + 3 * k2 + 4 * k3)

    return int_func


def ssprk3(func, return_im=False):
    """Third-order Strong Stability Preserving Runge-Kutta (SSPRK3).

    It has the characteristics of:

        - method stage = 3
        - method order = 3
        - Butcher Tables:

    .. math::

        \\begin{array}{c|ccc}
            0 & 0 & 0 & 0 \\\\
            1 & 1 & 0 & 0 \\\\
            1 / 2 & 1 / 4 & 1 / 4 & 0 \\\\
            \\hline & 1 / 6 & 1 / 6 & 2 / 3
        \\end{array}

    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + dt * k1, t + dt, *args)
        k3 = func(y0 + dt * k1 / 4 + dt * k2 / 4, t + dt / 2, *args)
        return y0 + dt / 6 * (k1 + k2 + 4 * k3)

    return int_func


def rk4(func, *args):
    """Classical fourth-order Runge-Kutta method for ordinary differential equations.

    It has the characteristics of:

        - method stage = 4
        - method order = 4
        - Butcher Tables:

    .. math::

        \\begin{array}{c|cccc}
            0 & 0 & 0 & 0 & 0 \\\\
            1 / 2 & 1 / 2 & 0 & 0 & 0 \\\\
            1 / 2 & 0 & 1 / 2 & 0 & 0 \\\\
            1 & 0 & 0 & 1 & 0 \\\\
            \\hline & 1 / 6 & 1 / 3 & 1 / 3 & 1 / 6
        \\end{array}

    """

    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + dt / 2 * k1, t + dt / 2, *args)
        k3 = func(y0 + dt / 2 * k2, t + dt / 2, *args)
        k4 = func(y0 + dt * k3, t + dt, *args)
        return y0 + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    return int_func


def ralston4(func, return_im=False):
    """Ralston's fourth-order method for ordinary differential equations.

    It has the characteristics of:

        - method stage = 4
        - method order = 4
        - Butcher Tables:

    .. math::

        \\begin{array}{c|cccc}
            0 & 0 & 0 & 0 & 0 \\\\
            .4 & .4 & 0 & 0 & 0 \\\\
            .45573725 & .29697761 & .15875964 & 0 & 0 \\\\
            1 & .21810040 & -3.05096516 & 3.83286476 & 0 \\\\
            \\hline & .17476028 & -.55148066 & 1.20553560 & .17118478
        \\end{array}

    References
    ----------

    [1] Ralston, Anthony (1962). "Runge-Kutta Methods with Minimum Error Bounds".
        Math. Comput. 16 (80): 431–437. doi:10.1090/S0025-5718-1962-0150954-0

    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + dt * k1 * 0.4, t + dt * 0.4, *args)
        k3 = func(y0 + dt * k1 * .29697761 + dt * k2 * .15875964, t + dt * .45573725, *args)
        k4 = func(y0 + dt * k1 * .21810040 + dt * k2 * -3.05096516 + dt * k3 * 3.83286476, t + dt, *args)
        return y0 + dt * (.17476028 * k1 + -.55148066 * k2 + 1.20553560 * k3 + .17118478 * k4)

    return int_func


def rk4_38rule(func, *args):
    """3/8-rule fourth-order method for ordinary differential equations.

    This method doesn't have as much notoriety as the "classical" method,
    but is just as classical because it was proposed in the same paper
    (Kutta, 1901).

    It has the characteristics of:

        - method stage = 4
        - method order = 4
        - Butcher Tables:

    .. math::

        \\begin{array}{c|cccc}
            0 & 0 & 0 & 0 & 0 \\\\
            1 / 3 & 1 / 3 & 0 & 0 & 0 \\\\
            2 / 3 & -1 / 3 & 1 & 0 & 0 \\\\
            1 & 1 & -1 & 1 & 0 \\\\
            \\hline & 1 / 8 & 3 / 8 & 3 / 8 & 1 / 8
        \\end{array}

    """
    dt = profile.get_dt()

    def int_func(y0, t, *args):
        k1 = func(y0, t, *args)
        k2 = func(y0 + dt / 3 * k1, t + dt / 3, *args)
        k3 = func(y0 - dt / 3 * k1 + dt * k2, t + 2 * dt / 3, *args)
        k4 = func(y0 + dt * k1 - dt * k2 + dt * k3, t + dt, *args)
        return y0 + dt / 8 * (k1 + 3 * k2 + 3 * k3 + k4)

    return int_func


