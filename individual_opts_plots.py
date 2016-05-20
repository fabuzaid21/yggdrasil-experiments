#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects):
  # attach some text labels
  for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., 1.02*height,
            '%d s' % int(height),
            ha='center', va='bottom')

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

plt.rc('text', usetex = True)
plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plt.rcParams.update({'font.size': 18})
plt.rcParams.update({'xtick.labelsize': 14}) 
#plt.rcParams.update({'figure.figsize': (5, 10)})

bars = plt.bar(index + bar_width / 2, times, bar_width, color='darkviolet')
autolabel(bars)

plt.ylabel('Training Time (s)')
plt.ylim([0, 150])
plt.title('Yggdrasil: Impact of Individual Optimizations')
plt.xticks(index + bar_width, xticks)
plt.tight_layout()
plt.savefig('Individual_Optimizations.eps')
