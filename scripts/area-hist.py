from __future__ import division
from __future__ import print_function
import numpy as np
import scipy.stats
from matplotlib import pyplot as plt
from matplotlib import ticker as mticker
from matplotlib import gridspec
import astropy.table
import os.path
import operator
# from common import *

keys = ('area90', 'searched-area')
labels = (r'area of 90\% confidence region (deg$^2$)', r'searched area (deg$^2$)')
# colors = np.asarray([[230, 159, 0], [86, 180, 233]]) / 255
colors = [[0.58, 0.15, 0.47], [0.19, 0.54, 0.71]]

fig = plt.figure(figsize=(6, 8.5))
gs = gridspec.GridSpec(5, 2, wspace=0.15, hspace=0.2)

for irun, run in enumerate(['2015', '2016']):
    filename = '../cbc/emfollowup/papers/first2years/data/{run}/{run}_coinc.txt'.format(run=run)
    data = astropy.table.Table.read(filename, format='ascii.cds')

    # Select only events that have LALInference localizations
    data = data[~data['pe-area90'].mask]

    for inet, net in enumerate(['HL', 'HV', 'LV', 'HLV']):
        group = data[data['network'] == net]
        if len(group) <= 0:
            continue
        for ikey, (key, label) in enumerate(zip(keys, labels)):
            # plt.figure(figsize=(3.5, 2.5))
            # plt.subplots_adjust(left=0.175, right=0.85, top=0.95, bottom=0.175)
            ax = fig.add_subplot(gs[irun + inet, ikey])
            ax.set_xlim(10, 1000)
            ax.set_xscale('log')
            ax.set_ylim(0, 100)
            ax.yaxis.set_major_formatter(mticker.FormatStrFormatter(r'%d\%%'))
            for complete, linestyle in zip([False, True], [':', '-']):
                if not complete and len(net) <= 2:
                    continue
                if complete:
                    group2 = group[reduce(operator.and_, [~group['snr-' + ifo].mask for ifo in net])]
                else:
                    group2 = group

                count_simulated_detections = float(len(group2))
                counts = np.arange(0, len(group2) + 1)
                pct = counts / count_simulated_detections * 100
                pct = np.concatenate((pct, [pct[-1]]))
                pct_ll, pct_ul = scipy.stats.beta.interval(0.95, counts + 1, count_simulated_detections - counts + 1)
                pct_ll *= 100
                pct_ul *= 100
                pct_ll = np.concatenate((pct_ll, [pct_ll[-1]]))
                pct_ul = np.concatenate((pct_ul, [pct_ul[-1]]))

                for pipe, color in zip(['rapid', 'pe'], colors):
                    areas = np.sort(np.asarray(group2[pipe + '-' + key]))
                    areas = np.concatenate(([1e-9], areas, [44100]))
    
                    ax.fill_between(
                        np.ravel(zip(areas[:-1], areas[1:])),
                        np.ravel(zip(pct_ll[1:], pct_ll[1:])),
                        np.ravel(zip(pct_ul[1:], pct_ul[1:])),
                        linewidth=0,
                        color=color,
                        alpha=0.4,
                    )
                    ax.plot(areas, pct, linestyle, drawstyle='steps-pre', color=color)
    
            ax.set_xlim(1, 10000)
            ax.set_ylim(0, 100)
            ax.set_yticks([50, 100])
            ax.grid()
            if ikey == 0:
                ax.set_yticklabels([])
                ax.set_ylabel('{}\n{}'.format(run, net), rotation=0, ha='right')
            else:
                ax.yaxis.tick_right()
            if irun + inet < 4:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel(label)
plt.savefig('area-hist.pdf'.format(run, net, key))
