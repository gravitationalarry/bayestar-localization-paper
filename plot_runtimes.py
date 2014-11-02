from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np

runtimes_2015 = np.load('2015_runtimes.npy')
runtimes_2016 = np.load('2016_runtimes.npy')

plt.figure(figsize=(3.5, 3))
ax = plt.axes()
artists = ax.violinplot(runtimes_2015.T, range(6), showextrema=False)
plt.setp(artists['bodies'], color='red')
artists = ax.violinplot(runtimes_2016.T, range(6), showextrema=False)
plt.setp(artists['bodies'], color='blue')
ax.xaxis.set_ticks(range(6))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: str(2**x)))
ax.set_yscale('log')
ax.set_ylim(10, 3000)
ax.set_xlabel('threads')
ax.set_ylabel('run time (s)')
plt.subplots_adjust(bottom=0.15)
plt.savefig('runtimes.pdf')
