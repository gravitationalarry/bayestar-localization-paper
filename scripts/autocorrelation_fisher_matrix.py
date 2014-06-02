"""Compute Fisher matrix for autocorrelation likelihood, using a TaylorF2
signal model."""
from __future__ import division
import numpy as np
import scipy.integrate
import scipy.interpolate
import scipy.special
import itertools
from lalinference.bayestar import filter
from lalinference.bayestar import timing

def abs2(x):
    return np.square(np.real(x)) + np.square(np.imag(x))

mass1 = 1.4
mass2 = 1.4
f_low = 40
S = timing.get_noise_psd_func('H1')

# Compute Fisher matrix elements for full signal (for comparison).
signal_model = timing.SignalModel(mass1, mass2, S, f_low,
    *timing.get_approximant_and_orders_from_string('TaylorF2threePointFivePN'))
w1 = signal_model.get_sn_moment(1)
w2 = signal_model.get_sn_moment(2)

# Compute 1 second of autocorrelation sequence.
# FIXME: make this the longest lag that we are going to integrate over.
acor_series, sample_rate = filter.autocorrelation(
    mass1, mass2, S, f_low, 1,
    *timing.get_approximant_and_orders_from_string('TaylorF2threePointFivePN'))

# Augment autocorrelation sequence with negative time lags.
n = len(acor_series)
t = np.arange(1-n, n) / sample_rate
acor_series = np.concatenate((np.conj(acor_series[:0:-1]), acor_series))

# Construct spline interpolant and derivatives for real part.
re_acor = scipy.interpolate.UnivariateSpline(t, acor_series.real, s=0, k=5)
re_acor_deriv = re_acor.derivative(1)
re_acor_deriv2 = re_acor.derivative(2)

# Construct spline interpolant and derivatives for imaginary part.
im_acor = scipy.interpolate.UnivariateSpline(t, acor_series.imag, s=0, k=5)
im_acor_deriv = im_acor.derivative(1)
im_acor_deriv2 = im_acor.derivative(2)

# Put real and imaginary parts back together.
def acor(t): return re_acor(t) + 1j * im_acor(t)
def acor_deriv(t): return re_acor_deriv(t) + 1j * im_acor_deriv(t)
def acor_deriv2(t): return re_acor_deriv2(t) + 1j * im_acor_deriv2(t)

def weight(a2, rho):
    rho2 = np.square(rho)
    Iarg = 0.25 * rho2 * a2
    exp = np.exp(0.5 * rho2 * (a2 - 1))
    return 0.5 * exp * (scipy.special.i0e(Iarg) + scipy.special.i1e(Iarg))

def den(t, rho):
    a = acor(t)
    a2 = abs2(a)
    rho2 = np.square(rho)
    exp = np.exp(0.5 * rho2 * (a2 - 1))
    return exp * scipy.special.i0e(0.25 * rho2 * a2)

def num_gamma_gamma(t, rho):
    a = acor(t)
    a2 = abs2(a)
    return a2 * weight(a2, rho)

def num_tau_tau(t, rho):
    a = acor(t)
    a2 = abs2(a)
    a_deriv2 = acor_deriv2(t)
    return -np.real(np.conj(a) * a_deriv2) * weight(a2, rho)

def num_gamma_tau(t, rho):
    a = acor(t)
    a2 = abs2(a)
    a_deriv = acor_deriv(t)
    return -np.imag(np.conj(a) * a_deriv) * weight(a2, rho)

def fisher_integral((T, num, rho)):
    args = (rho,)
    # All of the integrands are even, so we can integrate from 0 to T
    # instead of from -T to T.
    n, _ = scipy.integrate.quad(num, 0, T, args, limit=500)
    d, _ = scipy.integrate.quad(den, 0, T, args, limit=500)
    return n / d

def map_nested(map, func, *iterables):
    results = map(func, itertools.product(*iterables))
    return np.reshape(results, [len(iterable) for iterable in iterables])

if __name__ == '__main__':
    import json
    import multiprocessing

    snrs = np.logspace(-1, np.log10(30), 100)
    durations = [0.001, 0.01, 0.1, 1.]
    integrands = [num_gamma_gamma, num_tau_tau, num_gamma_tau]
    pool = multiprocessing.Pool()
    try:
        integrals = map_nested(
            pool.map, fisher_integral, durations, integrands, snrs)
    finally:
        pool.terminate()
    with open('autocorrelation_fisher_matrix.json', 'w') as outfile:
        json.dump({
            'snrs': snrs.tolist(),
            'durations': durations,
            'fisher_matrix_elements': (np.square(snrs) * integrals).tolist(),
            'w1': w1,
            'w2': w2
        }, outfile)
