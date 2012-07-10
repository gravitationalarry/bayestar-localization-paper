#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
"""
Create a figure that depicts the angular integration scheme.
"""
__author__ = "Leo Singer <leo.singer@ligo.org>"

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys

npoints = 15
u = np.arange(- (npoints // 2), np.ceil(npoints / 2)) / (npoints // 2)
phi = np.pi * u

phi, u = np.meshgrid(phi, u)

plt.figure(figsize=(5, 5))
plt.scatter(phi, u)
plt.ylim(-1.1, 1.1)
plt.xlim(-1.1*np.pi, 1.1*np.pi)
plt.xticks([-np.pi, 0, np.pi], [u'-π', '0', u'π'])
plt.yticks([-1, 0, 1])

if len(sys.argv) > 1:
    plt.savefig(sys.argv[1])
else:
    plt.show()
