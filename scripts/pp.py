import numpy as np
from matplotlib import pyplot as plt
from lalinference.bayestar import plot

fig = plt.figure(figsize=(3.5, 3.5))
ax = fig.add_subplot(111, projection='pp_plot')
ax.add_diagonal()

data = np.recfromtxt(
    '2015_subset/found_injections.out', names=True)['searched_prob']
n = len(data)
ax.add_series(data, label='2015')

data = np.recfromtxt(
    '2016_subset/found_injections.out', names=True)['searched_prob']
assert len(data) == n
ax.add_series(data, label='2016')

ax.add_confidence_band(n)
ax.legend(loc='lower right')
ax.set_xlabel('Credible level $p$')
ax.set_ylabel('Fraction of true locations with $\mathrm{CR}_p$')
ax.grid()

plt.savefig('pp.pdf')
