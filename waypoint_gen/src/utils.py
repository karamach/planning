from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
        
def plot(x, y, z):
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim(-200, 1200)
    ax.set_ylim(-500, 200)
    ax.set_zlim(0, 100)
    ax.plot(x, y, z, label='drone path', linestyle='--', marker='o')
    ax.legend()
    x_start = x == 0
    y_start = y == 0
    plt.scatter(x[x_start], y[y_start], color='green')     
    plt.show()
