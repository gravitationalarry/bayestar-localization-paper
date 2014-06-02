from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
import json

# Read data file
with open('autocorrelation_fisher_matrix.json', 'r') as infile:
    data = json.load(infile)

# Add dictionary entries to local namespace
locals().update(data)

fig = plt.figure(figsize=(3.5, 2.5))
fig.subplots_adjust(left=0.15, bottom=0.15)
ax = fig.add_subplot(111)
ax.set_xlabel('SNR')
ax.set_ylabel('Ratio')
ax.set_xlim(0, 8)
ax.set_ylim(0, 1)

colors = 'crgb'
for T, matrix_elements, color in reversed(zip(durations, fisher_matrix_elements, colors)):
    F11, F22, F12 = np.asarray(matrix_elements)
    ax.plot(snrs, F11 / np.square(snrs), '-', color=color)
    ax.plot(snrs, -F12 / (w1 * np.square(snrs)), '--', color=color)
    ax.plot(snrs, F22 / (w2 * np.square(snrs)), ':', color=color)

fig.savefig('fishfactor.pdf')
