# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib
matplotlib.rcParams['text.usetex'] = False
from lalinference import fits
from lalinference import cmap
from lalinference import plot
from wcsaxes import WCS
import numpy as np
from matplotlib import pyplot as plt
import healpy as hp
from matplotlib import collections
from matplotlib import patches
from matplotlib import ticker

ra0 = 130
dec0 = -10
phi0 = np.deg2rad(ra0)
theta0 = 0.5 * np.pi - np.deg2rad(dec0)
# ra0 = 137.8
# dec0 = -39.9
xyz0 = hp.ang2vec(0.5*np.pi - np.deg2rad(dec0), np.deg2rad(ra0))

prob, meta = fits.read_sky_map('../cbc/emfollowup/papers/first2years/data/2015/compare/18951/bayestar.fits.gz', nest=True)

def get_vertices(m):
    m = np.copy(m)
    top_npix = len(m)
    top_nside = hp.npix2nside(top_npix)
    top_order = int(np.log2(top_nside))
    for order in range(top_order + 1):
        nside = 1 << order
        npix = hp.nside2npix(nside)
        stride = 1 << (2 * (top_order - order))
        keep = (hp.pix2vec(nside, np.arange(npix), nest=True) * np.expand_dims(xyz0, 1)).sum(0) >= np.cos(np.deg2rad(30))
        if order < top_order:
            mm = m.reshape((-1, stride))
            keep &= (mm[:, :-1] == mm[:, 1:]).all(axis=1)
            m += hp.ud_grade(np.where(keep, np.nan, 0), nside_out=top_nside, order_in='NEST', order_out='NEST')
        else:
            keep &= ~np.isnan(m)
        for ipix in np.flatnonzero(keep):
            boundaries = hp.boundaries(nside, ipix, nest=True, step=1).T
            theta, phi = hp.vec2ang(boundaries)
            ra = np.rad2deg(phi)
            dec = np.rad2deg(0.5 * np.pi - theta)
            vertices = np.column_stack((ra, dec))
            yield vertices
vertices = list(get_vertices(prob))

fig = plt.figure(figsize=(3, 3))
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
ax = plt.axes(aspect=1)
ax.add_artist(collections.PolyCollection(
    vertices,
    closed=True,
    linewidths=0.5,
    edgecolors='0.6',
    facecolors='none'))
ax.set_xlim(ra0 + 20, ra0 - 20)
ax.set_ylim(dec0 - 20, dec0 + 20)

scalebar_dec = dec0 - 17.5
scalebar_ra0 = ra0 - 17.5
scalebar_dra = 10. / np.sin(theta0)
ax.plot(
    [scalebar_ra0, scalebar_ra0 + scalebar_dra],
    [scalebar_dec, scalebar_dec],
    color='black',
    linewidth=1)
ax.text(scalebar_ra0 + 0.5 * scalebar_dra, scalebar_dec + 1, u'10°', ha='center', va='baseline')
ax.set_xticks([])
ax.set_yticks([])
plt.savefig('adaptive_mesh.pdf')
