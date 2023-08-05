import numpy as np
import matplotlib.pyplot as plt


def show_graph(expression):
    x = np.arange(-10, 10, 0.1)
    y = expression

    plt.plot(x, y)
    plt.title("Graph")
    plt.xlabel("Values of x")
    plt.ylabel("Values of y")

    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)

    plt.show()