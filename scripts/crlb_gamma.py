from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
import json

# Read data file
with open('autocorrelation_fisher_matrix.json', 'r') as infile:
    data = json.load(infile)

# Add dictionary entries to local namespace
locals().update(data)

crlb1 = np.sqrt(w2 / (w2 - np.square(w1)))

fig = plt.figure(figsize=(3.5, 3.5))
fig.subplots_adjust(left=0.15)
ax = fig.add_subplot(111, aspect=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('SNR')
ax.set_ylabel('RMS phase error (rad)')
ax.set_ylim(1e-2, 1e1)
ax.grid()

for T, matrix_elements in reversed(zip(durations, fisher_matrix_elements)):
    F11, F22, F12 = np.asarray(matrix_elements)
    std_gamma = np.sqrt(F22 / (F11 * F22 - np.square(F12)))
    ax.plot(snrs, std_gamma, label=r'$T={0:g}$'.format(T))

snrs = np.asarray([1e-1, 1e2])
ax.plot(snrs, crlb1 / snrs, '--k', label=r'CRLB')

plt.legend(loc='lower left')
fig.savefig('crlb_gamma.pdf')
