from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import contour as mcontour
from matplotlib import gridspec as mgridspec
import scipy.special
from lalinference.bayestar import filter
from lalinference.bayestar import timing
import lal
import lalsimulation
import scipy.integrate
import scipy.signal
import os
import seaborn as sns
sns.set_style('white')

def abs2(a):
    return np.square(np.real(a)) + np.square(np.imag(a))

data = [
    ['LIGO-T1100338-v13-H1-SPECTRA-957474700-MODE.txt', "H1\nS6", False],
    ['LIGO-T1100338-v13-L1-SPECTRA-951280082-MODE.txt', "L1\nS6", False],
    ['LIGO-T1100338-v13-V1-SPECTRA-935662133-MODE.txt', "V1\nVSR2-3", False],
    ['LIGO-T0900288-v3-ZERO_DET_high_P.txt', "aLIGO\ndesign", True]
]

mass1 = mass2 = 1.4

fig = plt.figure(figsize=(11, 8.5))
gridspec = mgridspec.GridSpec(len(data), 3, wspace=0.1, hspace=0.1)

for i, (filename, label, need_square) in enumerate(data):
    path = os.path.join('psds', filename)
    f, S = np.loadtxt(path).T
    if need_square:
        S *= S
    S = timing.InterpolatedPSD(f, S)

    ax = fig.add_subplot(gridspec[i, 0])
    f = np.logspace(0, 4, 1000)
    ax.loglog(f, np.sqrt(S(f)), color='k')
    ax.set_ylabel(label, rotation='horizontal', ha='right', labelpad=20)
    ax.set_xlim(10, 1e4)
    ax.set_ylim(1e-24, 1e-21)
    if i == len(data) - 1:
        ax.set_xlabel('frequency (Hz)')
    else:
        plt.setp(ax.get_xticklabels(), visible=False)
    if i == 0:
        ax.set_title('Noise amp. spectral density')

    duration = lalsimulation.SimInspiralTaylorF2ReducedSpinChirpTime(
        10, mass1*lal.MSUN_SI, mass2*lal.MSUN_SI, 0,
        lalsimulation.PNORDER_THREE_POINT_FIVE)
    duration = int(np.ceil(filter.ceil_pow_2(duration)))
    sample_rate = 16384
    nsamples = duration * sample_rate
    nsamples_fft = nsamples//2 + 1
    af = lal.CreateCOMPLEX16Vector(nsamples)
    f = np.arange(nsamples) / duration

    hplus, hcross = lalsimulation.SimInspiralChooseFDWaveform(
        0, 1/duration,
        mass1*lal.MSUN_SI, mass2*lal.MSUN_SI,
        0, 0, 0, 0, 0, 0,
        9, 0, 40,
        500 * lal.PC_SI, 0, 0, 0,
        None, None,
        lalsimulation.PNORDER_THREE_POINT_FIVE,
        lalsimulation.PNORDER_NEWTONIAN, lalsimulation.TaylorF2)

    af.data[:len(hplus.data.data)] = abs2(hplus.data.data + 1j * hcross.data.data)
    af.data[len(hplus.data.data):] = 0
    af.data[0] = 0
    af.data[1:len(hplus.data.data)] /= S(f[1:len(hplus.data.data)])

    a = lal.CreateCOMPLEX16Vector(nsamples)
    plan = lal.CreateReverseCOMPLEX16FFTPlan(nsamples, 0)
    lal.COMPLEX16VectorFFT(a, af, plan)

    a = a.data
    b = np.abs(a)
    a /= np.max(b)
    b /= np.max(b)
    n = sample_rate

    ax = fig.add_subplot(gridspec[i, 1])
    t = np.arange(-n+1, n)/sample_rate
    ax.set_yscale('log')
    ax.set_xlim(-25, 25)
    ax.set_ylim(1e-2, 2)
    # ax.semilogy(t*1000, np.concatenate((b[n-1:0:-1], b[:n])), color='k')
    ax.fill_between(t*1000, np.concatenate((b[n-1:0:-1], b[:n])), color=sns.color_palette('GnBu_d', 4)[1])

    if i == len(data) - 1:
        ax.set_xlabel('time delay (ms)')
    else:
        plt.setp(ax.get_xticklabels(), visible=False)

    if i == 0:
        ax.set_title('Autocorrelation function')
    plt.setp(ax.get_yticklabels(), visible=False)

#     ax = fig.add_subplot(gridspec[i, 2])
#     ax.set_yscale('log')
#     t = np.arange(-n+1, n)/sample_rate
#     for rho, linestyle in [[1, '--'], [2, '-.'], [4, ':'], [8, '-']]:
#         rho2 = np.square(rho)
#         acor = np.concatenate((b[n-1:0:-1], b[:n]))
#         iarg = rho2 * acor
#         iarg0 = rho2
#         like = scipy.special.i0e(iarg) / scipy.special.i0e(iarg0) * np.exp(iarg - iarg0)
#         if i == 0 and j == len(masses) - 1:
#             label = r'SNR=%d' % rho
#         else:
#             label = label
#         ax.semilogy(
#             t*1000,
#             scipy.special.i0e(iarg) / scipy.special.i0e(iarg0) * np.exp(iarg - iarg0),
#             linestyle,
#             color='k',
#             label=label)
#     ax.set_xlim(-25, 25)
#     ax.set_ylim(1e-2, 2)
#     ax.legend(loc='upper right', fontsize=9)

#     if i == len(data) - 1:
#         ax.set_xlabel('time delay (ms)')
#     else:
#         plt.setp(ax.get_xticklabels(), visible=False)

#     if i == 0:
#         ax.set_title(r'$(%g, %g) M_\odot$' % (mass1, mass2))
    #     if j == len(masses) - 1:
    #         ax.yaxis.tick_right()
    #         ax.set_ylabel('likelihood')
    #         ax.yaxis.set_label_position('right')
    #     else:
    #         plt.setp(ax.get_yticklabels(), visible=False)

    ax = fig.add_subplot(gridspec[i, 2])
    ax.set_yscale('log')
    t = np.arange(-n+1, n)/sample_rate
    for (rho, linestyle), color in zip([[1, '--'], [2, '-.'], [4, ':'], [8, '-']], sns.color_palette('GnBu_d', 4)):
        rho2 = np.square(rho)
        acor = np.concatenate((b[n-1:0:-1], b[:n]))
        iarg = rho2 * acor
        iarg0 = rho2
        like = scipy.special.i0e(iarg) / scipy.special.i0e(iarg0) * np.exp(iarg - iarg0)
        #ax.semilogy(
        #    rho*t*1000,
        #    scipy.special.i0e(iarg) / scipy.special.i0e(iarg0) * np.exp(iarg - iarg0),
        #    linestyle,
        #    color='k',
        #    label=label)
        x = rho*t*1000
        y = scipy.special.i0e(iarg) / scipy.special.i0e(iarg0) * np.exp(iarg - iarg0)
        # ax.plot(x, y, color='black')
        ax.fill_between(x, y, color=color)
    if i == 0:
        ax.text(15, 0.2, 'S/N=1', color='white', va='center')
        ax.text(15, 0.06, 'S/N=2', color='white', va='center')
        ax.annotate('S/N=4', (5, np.sqrt(0.06 * 0.015)), (15, np.sqrt(0.06 * 0.015)), textcoords='data', color='white', va='center',
            arrowprops=dict(arrowstyle='->', color='white'))
        ax.annotate('S/N=8', (4, 0.015), (15, 0.015), textcoords='data', color='white', va='center',
            arrowprops=dict(arrowstyle='->', color='white'))
    ax.set_xlim(-25, 25)
    ax.set_ylim(1e-2, 2)

    if i == len(data) - 1:
        ax.set_xlabel(r'SNR $\times$ time delay (ms)')
    else:
        plt.setp(ax.get_xticklabels(), visible=False)

    if i == 0:
        ax.set_title('Likelihood')
    ax.yaxis.tick_right()
    # if j == len(masses) - 1:
    #     ax.yaxis.tick_right()
    #     # ax.set_ylabel('likelihood')
    #     ax.yaxis.set_label_position('right')
    # else:
    #     plt.setp(ax.get_yticklabels(), visible=False)
fig.savefig('autocorr-likelihood.png')