#!/usr/bin/env python

from utils import save_figure
import matplotlib.pyplot as plt
import numpy as np
import config

# attach wall-clock time at top of bar
def autolabel(rects):
  for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., 1.02*height,
            '%d s' % int(height), ha='center', va='bottom')

# - sort in place
# - sort in place + sparse bitvectors
# - sort in place + sparse bitvectors + compressed labels 
# - sparse bitvectors + compressed labels + RLE + node indices 
xticks = (
    'uncompressed\ntraining',
    'uncompressed +\nsparse bitvectors',
    'uncompressed +\nsparse bitvectors +\nlabel encoding',
    'RLE +\nsparse bitvectors +\nlabel encoding'
)
times = [134.467, 125.764, 101.054, 81.51]
bar_width = 0.35*3
index = np.arange(0, len(times)*3, 3)

if __name__ == '__main__':
    plt.rcParams.update({'xtick.labelsize': 15})
    plt.rcParams.update({'figure.figsize': (10, 6)})

    bars = plt.bar(index + bar_width / 2, times, bar_width,
                   color='darkviolet')
    autolabel(bars)

    plt.title('Yggdrasil: Impact of Individual Optimizations', y=1.04)
    plt.ylabel('Training Time (s)')
    plt.ylim([0, 150])
    plt.xlim([0, 11])
    plt.xticks(index + bar_width, xticks)
    plt.tight_layout()
    print 'individual_optimizations.svg'
    plt.savefig('individual_optimizations.svg', transparent=True,
                pad_inches=2.5)
    #print 'individual_optimizations.eps'
    #plt.savefig('individual_optimizations.eps')

