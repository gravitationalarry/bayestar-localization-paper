#!/usr/bin/env python
from __future__ import division
"""
Create a figure that depicts the subdivision technique for the radial integral.
"""
__author__ = "Leo Singer <leo.singer@ligo.org>"

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import BboxConnectorPatch
from matplotlib.transforms import Bbox, TransformedBbox, blended_transform_factory
from matplotlib import ticker
from scipy import special
import numpy as np
import sys

xmin = 0.
xmax = 1.
a = 0.1
a2 = a * a
y1 = 0.01
y2 = 0.005
break1 = (a - a2 * np.sqrt(-2*np.log(y1))) / (1 + 2 * a2 * np.log(y1))
if a * np.sqrt(-2 * np.log(y2)) < 1:
    break2 = (a + a2 * np.sqrt(-2*np.log(y1))) / (1 + 2 * a2 * np.log(y1))
else:
    break2 = (np.log(y2) - np.sqrt(np.log(y1) * np.log(y2))) / (np.sqrt(-2*np.log(y2)) * (np.log(y2) - np.log(y1)))

breakpoints = [xmin]
if xmin < break1 < xmax:
    breakpoints.append(break1)
if xmin < break2 < xmax:
    breakpoints.append(break2)
breakpoints.append(xmax)

colors = 'rgb'
fig = plt.figure(figsize=(5, 5))
ax0 = plt.axes([0.2, 0.5, 0.6, 0.4])

for i, (break1, break2) in enumerate(zip(breakpoints[:-1], breakpoints[1:])):
    x = np.linspace(break1, break2, 100)
    I0e = special.i0e(1 / a2)
    lognorm = - 1 / (2 * a2) - np.log(I0e)
    I0e = special.i0e(1 / (a * x))
    integrand = I0e * np.exp(-1/(2*x*x) + lognorm + 1 / (a * x))
    plt.fill_between(x, np.zeros(x.shape), integrand, color=colors[i])
plt.xlim(xmin, xmax)
ax0.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
trans0 = blended_transform_factory(ax0.transData, ax0.transAxes)
plt.setp(ax0.get_xticklabels(), visible=False)
plt.setp(ax0.get_yticklabels(), visible=False)
ax = None
nsubplots = len(zip(breakpoints[:-1], breakpoints[1:]))



for i, (break1, break2) in enumerate(zip(breakpoints[:-1], breakpoints[1:])):
    ax = plt.axes([0.1 + 0.8 / nsubplots * i - 0.025 * (nsubplots - i - 3), 0.1, 0.8 / nsubplots - 0.05, 0.3], sharey=ax0)

    d = .045 # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)

    if i > 0:
        ax.spines['left'].set_visible(False)
        ax.tick_params(left=False)
        ax.plot((-d,d),(-d,+d), **kwargs) # top-right diagonal
        ax.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal
    if i < nsubplots - 1:
        ax.spines['right'].set_visible(False)
        ax.tick_params(right=False)
        ax.plot((1-d,1+d),(-d,+d), **kwargs) # top-left diagonal
        ax.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-left diagonal
    fig.subplots_adjust(wspace=0.15)
    bbox0 = Bbox.from_extents(break1, 0, break2, 1)
    mybbox0 = TransformedBbox(bbox0, trans0)
    fig.artists.append(BboxConnectorPatch(ax.bbox, mybbox0, 1, 4, 2, 3, facecolor='none', linestyle='dashed'))
    if i > 0:
        plt.setp(ax.get_yticklabels(), visible=False)
    x = np.linspace(break1, break2, 100)
    I0e = special.i0e(1 / a2)
    lognorm = - 1 / (2 * a2) - np.log(I0e)
    I0e = special.i0e(1 / (a * x))
    integrand = I0e * np.exp(-1/(2*x*x) + lognorm + 1 / (a * x))
    plt.fill_between(x, np.zeros(x.shape), integrand, color=colors[i])
    plt.xlim(break1, break2)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.ylim(-.1, 1.1)


if len(sys.argv) > 1:
    plt.savefig(sys.argv[1])
else:
    plt.show()
