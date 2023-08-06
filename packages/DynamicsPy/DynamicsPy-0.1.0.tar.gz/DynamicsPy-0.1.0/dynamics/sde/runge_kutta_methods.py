# -*- coding: utf-8 -*-


from dynamics import profile
from dynamics import backend


__all__ = [
    'euler',
    'heun',
    'milstein_Ito',
    'milstein_Stra',
]


def euler(func):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def int_func(y0, t, *args):
        dfdg = func(y0, t, *args)
        dfdt = dfdg[0] * dt
        dW = backend.standard_normal(backend.shape(y0))
        dgdt = dt_sqrt * dfdg[1] * dW
        return y0 + dfdt + dgdt

    return int_func


def heun(func, *args):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def int_func(y0, t, *args):
        dfdg = func(y0, t, *args)
        df = dfdg[0]
        dg = dfdg[1]
        dfdt = df * dt
        dW = backend.standard_normal(backend.shape(y0))
        y_bar = y0 + dg * dW * dt_sqrt
        dg_bar = func(y_bar, t, *args)[1]
        dgdW = 0.5 * (dg + dg_bar) * dW * dt_sqrt
        y = y0 + dfdt + dgdW
        return y

    return int_func


def milstein_Ito(func, *args):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def int_func(y0, t, *args):
        dW = backend.standard_normal(backend.shape(y0))
        dfdg = func(y0, t, *args)
        df = dfdg[0]
        dg = dfdg[1]
        dfdt = df * dt
        dgdW = dg * dW * dt_sqrt
        df_bar = y0 + dfdt + dg * dt_sqrt
        dg_bar = func(df_bar, t, *args)[1]
        extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt - dt_sqrt)
        return y0 + dfdt + dgdW + extra_term

    return int_func


def milstein_Stra(func, *args):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def int_func(y0, t, *args):
        dW = backend.standard_normal(backend.shape(y0))
        dfdg = func(y0, t, *args)
        df = dfdg[0]
        dg = dfdg[1]
        dfdt = df * dt
        dgdW = dg * dW * dt_sqrt
        df_bar = y0 + dfdt + dg * dt_sqrt
        dg_bar = func(df_bar, t, *args)[1]
        extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt)
        return y0 + dfdt + dgdW + extra_term

    return int_func
