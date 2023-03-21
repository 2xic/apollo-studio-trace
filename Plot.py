import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import norm

def scatter(
        x,
        y,
        label,
        xlabel,
        ylabel,
):
    plt.scatter(x, y, label=label)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)

def scatter_3d(
        ax,
        x,
        y,
        z,
        symbol,
        label,
):
    ax.plot(
        x, 
        y, 
        z, 
        symbol,
        label=label,
    )

def gaussian(time_usage, label):
    mu = np.mean(time_usage)
    variance = np.var(time_usage)
    sigma = math.sqrt(variance)

    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    plt.plot(x, norm.pdf(x, mu, sigma), label=label)
    plt.xlabel('Response time')

def histogram(time_usage, label):
    plt.hist(time_usage, bins=list(map(lambda x: x * 1000, range(20))), label=label)
    plt.xlabel('Response time')
    plt.ylabel('Requests')
