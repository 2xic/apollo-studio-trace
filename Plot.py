import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import norm

def gaussian(time_usage, label):
    mu = np.mean(time_usage)
    variance = np.var(time_usage)
    sigma = math.sqrt(variance)

    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x, norm.pdf(x, mu, sigma), label=label)
