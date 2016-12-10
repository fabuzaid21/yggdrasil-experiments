#!/usr/bin/env python

from utils import save_figure
import matplotlib.pyplot as plt
import numpy as np
import sys
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
COLORS = ['orangered', '#814b91', '#814b91', '#814b91']
Y_MAX = 150
BAR_WIDTH = 0.29
x_indices = np.arange(0, len(times))
bar_indices = x_indices + BAR_WIDTH / 2
X_MAX = bar_indices[-1] + 3*BAR_WIDTH / 2

N = int(sys.argv[-1]) if len(sys.argv[1:]) == 1 else 4

if __name__ == '__main__':
    plt.rcParams.update({'xtick.labelsize': 13})
    plt.rcParams.update({'figure.figsize': (8, 6.5)})

    _, ax = plt.subplots()
    ax.set_title('Yggdrasil: Impact of Individual Optimizations', y=1.04)
    ax.set_ylabel('Training Time (s)')
    ax.set_ylim([0, Y_MAX])
    ax.set_xlim([0, X_MAX])
    ax.set_axisbelow(True)


    bars = ax.bar(bar_indices[:N], times[:N], BAR_WIDTH, color=COLORS)
    autolabel(bars)
    plt.xticks(x_indices[:N] + BAR_WIDTH, xticks[:N])
    plt.tight_layout()

    print 'individual_optimizations_%d.pdf' % N
    plt.grid(b=True, axis='y')
    plt.savefig('individual_optimizations_%d.pdf' % N, transparent=True,
                pad_inches=0.05)

