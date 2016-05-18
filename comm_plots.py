#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

by_col_2000 = [87e3, 101.8e3, 129.8e3, 184.7e3, 292.2e3, 503e3, 918.1e3,
               1739.4e3, 3.3e6, 6.4e6]
#by_col_4000 = [86.5e3, 101.9e3, 130.1e3, 185.3e3, 293.1e3, 503.2e3, 918.3e3,
#               1741.6e3, 3.3e6, 6.5e6]
by_row_1000 = [49.7e6, 98.3e6, 194.9e6, 387.6e6, 772.8e6, 1540.9e6, 2.9e9,
        4.7e9, 6.2e9, 7.3e9 + 22.8e6]
by_row_2000 = [98.5e6, 195.4e6, 388.2e6, 771.1e6, 1541e6, 2.8e9, 4.8e9, 7.0e9,
        9.4e9, 6.2e9 + 6.29e9 + 17.2e6]
by_row_4000 = [197.5e6, 391.1e6, 776.2e6, 1546.3e6, 3e9, 5.9e9, 10.7e9, 15.7e9,
                10.6e9 + 9.7e9, 6.6e9 + 6.5e9 + 5.0e9 + 6.9e9 + 683.9e6]
x_axis = range(1, 11)

plt.rc('text', usetex = True)
plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plt.rcParams.update({'font.size': 18})

ygg, = plt.plot(x_axis, np.cumsum(by_col_2000), '.-', markersize=10, label='Yggdrasil, p = \{1K, 2K, 4K\}', color='g')

#plt.plot(x_axis, np.cumsum(by_col_4000), '.-', label='Yggdrasil, p = 4000')
planet_1k, = plt.plot(x_axis, np.cumsum(by_row_1000), 'x-', markersize=10, label='PLANET, p = 1K', color='b')
planet_2k, = plt.plot(x_axis, np.cumsum(by_row_2000), 'x-', markersize=10, label='PLANET, p = 2K', color='cyan')
planet_4k, = plt.plot(x_axis, np.cumsum(by_row_4000), 'x-', markersize=10, label='PLANET, p = 4K', color='red')

first_legend = plt.legend(handles=[planet_1k, planet_2k, planet_4k], loc='upper left',
                          fontsize='15')
ax = plt.gca().add_artist(first_legend)
plt.legend(handles=[ygg], loc='lower right', fontsize='15')
plt.ylabel('Number of Bytes Sent, Log Scale')
plt.xlabel('Tree Depth')
plt.title('Yggdrasil vs. PLANET: Communication Cost')
plt.yscale('log')
plt.grid(True)
plt.savefig('Communication.eps')
