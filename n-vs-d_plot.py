#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from math import log
from scipy.special import lambertw

def ticks_format(value, index):
    """
    Converts to labels to scientific notation: n*e^m
    To have all the number of the same size they are all returned as latex strings
    """
    if not(index == 1 or index == 4 or index == 7 or index == 15):
        return ''
    exp = np.floor(np.log10(value))
    base = value/10**exp
    return '${0:d}e^{{{1:d}}}$'.format(int(base), int(exp))

plt.rc('text', usetex = True)
plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plt.rcParams.update({'font.size': 18})

n_s_args = (5e5, 8.5e6, 5e5)
#p_s_args = (500, 4000, 500)
#d_s = np.linspace(5, 20, 16)

p = 2500.0
B = 32.0
k = 16.0

d = lambda n: -2.1*lambertw(((8*(1 - 4*p*B)*log(2.0))/n), 1)/log(2.0)#1e3*(D / (pow(2, D) *B))*(n/32.0) + (1/4*B)

n_s_points = np.linspace(*n_s_args)
y_s = [d(n) for n in n_s_points]
fig, ax = plt.subplots()
#ax.fill_between(n_s_points, 0, y_s)
#ax.fill_between(n_s_points, y_s, 4000, facecolor='orange')
ax.plot(n_s_points, y_s, '-')

#plt.xticks(n_s)
ax.set_xscale('log')
ax.set_xlim([n_s_args[0], n_s_args[1]])
ax.set_xticks(np.arange(*n_s_args))
ax.xaxis.set_major_formatter(FuncFormatter(ticks_format))
#ax.xaxis.set_minor_formatter(FuncFormatter(ticks_format))
#for label in line.axes.get_xaxis().get_ticklabels()[::2]:
#    label.set_visible(True)
#plt.yticks(np.arange(*p_s_args))

#plt.legend(loc='lower left', fontsize='15')
plt.ylabel('Tree Depth (D)')
plt.xlabel('Num. Instances (n), Log Scale')
plt.grid(True)
plt.savefig('n-vs-d.eps')
