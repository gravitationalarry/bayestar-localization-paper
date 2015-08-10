import numpy as np
from matplotlib import pyplot as plt
from lalinference.bayestar.sky_map import LogRadialIntegrator
from astropy.utils.console import ProgressBar

fig = plt.figure(figsize=(3.5, 2.5))
ax = fig.add_subplot(111)

r1 = 0.0
r2 = 0.25
k = 2
pmax = 1.0

np.random.seed(0)
nruns = 10
x = np.random.uniform(-5, np.log(pmax), nruns)
y = np.random.uniform(-5, 5, nruns)
p = np.exp(x)
b = 2 * np.exp(2*x - y)

npoints = np.unique(np.round(np.logspace(np.log10(2), 3, 50)).astype(int))
data = np.empty((len(npoints), len(p)))

for i, n in enumerate(ProgressBar(npoints)):
    integrator = LogRadialIntegrator(r1, r2, k, pmax, n)
    data[i] = [integrator(*_) for _ in zip(p, b)]

relerr = np.abs(np.exp(data[:-1] - data[-1]) - 1)
npoints = npoints[:-1]
ax.plot(npoints, relerr, '-k')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(1e-10, 1)
ax.set_xlabel('number of grid points')
ax.set_ylabel('relative error')

fig.subplots_adjust(left=0.175, bottom=0.15, right=0.95, top=0.95)

fig.savefig('distance_interpolant_convergence.pdf')
