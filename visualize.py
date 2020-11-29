# Visualizes spatial grid with values at location points
import matplotlib.pyplot as plt
import numpy as np

# x = horizontal points grid, y = vertical points grid, data = values
def visualize(x, y, vals):
    fig = plt.figure()
    plt.scatter(x, y, c=vals, cmap='viridis')
    plt.colorbar()
    
