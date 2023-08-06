import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from dynamics import ode

Axes3D


def lorenz_system():
    sigma = 10
    beta = 8 / 3
    rho = 28

    @ode.rk4
    def integral(state, t):
        x, y, z = state
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        return np.array([dx, dy, dz])

    times = np.arange(0, 100, 0.01)
    mon = []
    state = np.ones(3)
    for t in times:
        state = integral(state, t)
        mon.append(state)
    mon = np.array(mon)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    plt.plot(mon[:, 0], mon[:, 1], mon[:, 2])
    ax.set_xlabel('x')
    ax.set_xlabel('y')
    ax.set_xlabel('z')

    plt.show()


lorenz_system()







