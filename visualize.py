import matplotlib.pyplot as plt
import numpy as np

def visualize(x, y, vals):
    fig = plt.figure()
    plt.scatter(x, y, c=vals, cmap='viridis')
    plt.colorbar()
    plt.show()
