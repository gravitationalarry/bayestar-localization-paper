from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
import scipy.integrate
import scipy.special

r1 = 0
r2 = 0.25
pmax = np.sqrt(0.5 * 3)
k = 2

def integrand(r, p, b, k):
    return np.exp(-np.square(p/r - 0.5*b/p)) * scipy.special.i0e(b / r) * r**k

@np.vectorize
def integral(p, b, k):
    value, error = scipy.integrate.quad(integrand, r1, r2, args=(p, b, k))
    return value

SQRT2 = np.sqrt(2)
alpha = 4.0
p0 = 0.5 * (r2 if k >= 0 else r1)
x0 = np.log(min(p0, pmax))
xmin = x0 - (1 + SQRT2) * alpha
xmax = np.log(pmax)
ymin = 2 * x0 - SQRT2 * alpha - xmax
ymax = x0 + alpha

x = np.linspace(xmin - 4, xmax, 200)
y = np.linspace(ymin - 4, ymax + 4, 200)
xx, yy = np.meshgrid(x, y)

p = np.exp(xx)
r0 = np.exp(yy)
b = 2*np.square(p) / r0
z = integral(p, b, k)

fig = plt.figure(figsize=(3, 3))
ax = plt.subplot(111, aspect=1)
ax.imshow(z, origin='lower left', extent=[x.min(), x.max(), y.min(), y.max()], cmap='cool')
ax.contour(x, y, z, levels=np.logspace(-4, np.log10(z.max()), 6), colors='black')
ax.axvspan(xmax, xmax + 4, color='lightgray', alpha=0.25)

# ax.set_frame_on(False)
ax.set_xticks([x0 - (1 + SQRT2) * alpha, x0, xmax])
for tick in ax.get_xticks():
    ax.axvline(tick, color='black', linewidth=0.5, alpha=0.25)
ax.set_xticklabels([r'$x_\mathrm{min}$', r'$x_0$', r'$x_\mathrm{max}$'])
ax.set_yticks([2 * x0 - SQRT2 * alpha - xmax, x0, x0 + alpha])
for tick in ax.get_yticks():
    ax.axhline(tick, color='black', linewidth=0.5, alpha=0.25)
ax.set_yticklabels([r'$y_\mathrm{min}$', r'$x_0$', r'$y_\mathrm{max}$'])
ax.set_xlim(xmin - 4, xmax + 4)
ax.plot(np.linspace(xmin, xmax), np.linspace(ymax, ymin), color='k', linewidth=1.5)
_ = np.linspace(xmin - 4, xmax)
ax.plot(_, ymax * np.ones_like(_), color='k', linewidth=1.5)
_ = np.linspace(ymin - 4, ymax + 4)
ax.plot(xmax * np.ones_like(_), _, color='k', linewidth=1.5)
ax.text(0.4 * xmin + 0.6 * xmax, x0 + 1, 'I', fontsize='x-large')
ax.text(0.5 * (x.min() + xmax), ymax + 1.5, 'II', fontsize='x-large')
ax.text(xmin + 1, 0.5 * (ymin + x0), 'III', fontsize='x-large')
plt.savefig('radial_integral_interpolant.pdf')