#!/usr/bin/env python
"""
Plot the distribution of angular offset for an uninformative sky location
estimator.
"""
__author__ = "Leo Singer <leo.singer@ligo.org>"

from matplotlib import pyplot as plt
import numpy as np

theta = np.logspace(np.log10(0.1), np.log10(180), 1000)
p = np.square(np.sin(np.deg2rad(theta)))
plt.semilogx(theta, p)
plt.xlim(0.1, 1000)
plt.ylim(0, 1.2)
plt.grid()
plt.xlabel('angle between true location and mode of posterior')
plt.ylabel('probability density')
plt.title(r'totally uninformative localization: $f(\theta) = \, \frac{2}{\pi} \, \sin^2 \theta$')
plt.setp(plt.gca().get_yticklabels(), visible=False)
plt.savefig('uninformative.pdf')
