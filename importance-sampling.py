#!/usr/bin/env python
import matplotlib
matplotlib.rcParams['text.usetex'] = False
import seaborn
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import scipy.stats
import scipy.special
seaborn.set_style('white')

gcolor, fcolor = seaborn.color_palette('deep', 2)


def Q(x):
    return scipy.stats.norm.sf(x)

nsamp = 500

r0 = 0.33
p = 1.07
nrmin = 130
nrmax=-240
b = 2 * np.square(p) / r0

r = np.linspace(0, 1, nsamp)
diff = p/r - 0.5*b/p
diff2 = np.square(diff)

f = np.exp(-diff2) * np.square(r/r0)
g = np.exp(-diff2) / np.square(r / r0)
G = np.sqrt(np.pi) / p * Q(np.sqrt(2) * diff)
fg = scipy.special.i0e(b / r) * np.square(r / r0) * np.square(r)

# nrmin = 110
# nrmax = -200
rmin = r[nrmin]
rmax = r[nrmax]
Gmin = G[nrmin]
Gmax = G[nrmax]

common_line_style = {'color': 'black', 'linewidth': 1}
connecting_common_line_style = {'color': 'black', 'linewidth': 1}

fig = plt.figure(figsize=(5, 5))
gs = GridSpec(2, 2)
ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[1, 0], sharex=ax0)
ax2 = fig.add_subplot(gs[1, 1], sharey=ax1)
ax3 = fig.add_subplot(gs[0, 1], sharex=ax2, sharey=ax0, frameon=False)

ax0.fill_between(r[:nrmin], f[:nrmin] / np.nanmax(f), alpha=0.5, color=fcolor)
ax0.fill_between(r[nrmax:], f[nrmax:] / np.nanmax(f), alpha=0.5, color=fcolor)
ax0.fill_between(r[nrmin:nrmax], f[nrmin:nrmax] / np.nanmax(f), color=fcolor)
ax0.plot(r, g / np.nanmax(g), color=gcolor, alpha=0.5)
ax0.plot(r[nrmin:nrmax], g[nrmin:nrmax] / np.nanmax(g), color=gcolor)
ax0.set_xlim(r[0], r[-1])
ax0.set_ylim(0, 1.25)
ax1.plot(r, G, color=gcolor, alpha=0.5)
ax1.plot(r[nrmin:nrmax], G[nrmin:nrmax], color=gcolor)
ax1.set_ylim(G[0], G[-1])
ax2.fill_betweenx(G[:nrmin], fg[:nrmin], alpha=0.5, color=fcolor)
ax2.fill_betweenx(G[nrmax:], fg[nrmax:], alpha=0.5, color=fcolor)
ax2.fill_betweenx(G[nrmin:nrmax], fg[nrmin:nrmax], color=fcolor)

ax0.set_xticks([rmin, rmax])
ax0.set_xticklabels([r'$r_\mathrm{min}$', r'$r_\mathrm{max}$'])
ax0.set_yticks([])
ax0.text(0.2, 0.75, r'$g(r)$', ha='right', color=gcolor, fontsize='large')
ax0.text(0.725, 0.75, r'$f(r)$', ha='right', color=fcolor, fontsize='large')
plt.setp(ax0.get_xticklabels(), visible=False)
ax0.set_title('Original integrand')
ax1.set_xlabel('Change of variables')
ax2.set_title('Transformed integrand')

for r in (rmin, rmax):
    for ax in (ax0, ax1):
        ax.axvline(r, **common_line_style)
    _, top = (ax0.transAxes - ax1.transAxes).transform([0, 1])
    ax1.axvline(r, -0.05, top, clip_on=False, linewidth=0.5, color='black')

for G in (Gmin, Gmax):
    for ax in (ax1, ax2):
        ax.axhline(G, **common_line_style)
    right, _ = (ax2.transAxes - ax1.transAxes).transform([1, 0])
    ax1.axhline(G, -0.05, right, clip_on=False, linewidth=0.5, color='black')

ax3.annotate('', (0.5, 0), (0, 0.5), 'axes fraction', 'axes fraction', color='black', arrowprops=dict(arrowstyle='->', linewidth=1, color='black', connectionstyle='angle,angleA=0,angleB=90'))

ax1.set_yticks([Gmin, Gmax])
ax1.set_yticklabels([r'$G_\mathrm{min}$', r'$G_\mathrm{max}$'])

ax2.set_xlim(0, 0.5 * np.mean(fg))
ax2.set_xticks([])
ax2.set_xlabel(r'$\frac{f}{g}$')
plt.setp(ax2.get_yticklabels(), visible=False)

plt.setp(ax3.get_xticklabels(), visible=False)
plt.setp(ax3.get_yticklabels(), visible=False)
fig.savefig('importance-sampling.pdf')
