#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from math import pow
from math import log
from scipy.special import lambertw

def x_ticks_format(value, index):
    """
    Converts to labels to scientific notation: n*e^m
    To have all the number of the same size they are all returned as latex strings
    """
    exp = np.floor(np.log10(value))
    base = value/10**exp
    if not(index == 1 or index == 4 or index == 7 or index == 15):
      return ''
    if index == 1:
      return '$n$'
    return '${0:d}n$'.format(int(base))

def y_ticks_format_features(value, index):
    """
    Converts to labels to scientific notation: n*e^m
    To have all the number of the same size they are all returned as latex strings
    """
    #exp = np.floor(np.log10(value))
    #base = value/10**exp
    if index == 0:
      return ''
    if index == 1:
      return '$p$'
    return '${0:d}p$'.format(index)

def y_ticks_format_depth(value, index):
    """
    Converts to labels to scientific notation: n*e^m
    To have all the number of the same size they are all returned as latex strings
    """
    #exp = np.floor(np.log10(value))
    #base = value/10**exp
    if index == 0:
      return ''
    if index == 1:
      return '$D$'
    return '${0:d}D$'.format(index)



plt.rc('text', usetex = True)
plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plt.rcParams.update({'font.size': 18})

n_s_args = (5e5, 8.5e6, 5e5)
p_s_args = (500, 4000, 500)
#d_s = np.linspace(5, 20, 16)

D = 15.0
B = 32.0
k = 16.0

p = lambda n: 1e3*(D / (pow(2, D) *B))*(n/32.0) + (1/4*B)

plt.rc('text', usetex = True)
plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plt.rcParams.update({'font.size': 18})

n_s_points = np.linspace(*n_s_args)
y_s = [p(n) for n in n_s_points]
fig, ax = plt.subplots(2, figsize=(7.5, 8), sharex=True)

#ax.fill_between(n_s_points, 0, y_s)
#ax.fill_between(n_s_points, y_s, 4000, facecolor='orange')
ax[0].plot(n_s_points, y_s, '-')

#plt.xticks(n_s)
ax[0].set_xscale('log')
ax[0].set_xlim([n_s_args[0], n_s_args[1]])
ax[0].set_xticks(np.arange(*n_s_args))
ax[0].xaxis.set_major_formatter(FuncFormatter(x_ticks_format))
ax[0].yaxis.set_major_formatter(FuncFormatter(y_ticks_format_features))
ax[0].set_title('Communication Cost: Yggdrasil vs. Spark MLlib')
ax[0].text(2.25e6, 350, 'Spark MLlib Better',
      bbox={'facecolor':'powderblue', 'alpha':0.5, 'pad':10})
ax[0].text(8e5, 2700, 'Yggdrasil Better',
      bbox={'facecolor':'orange', 'alpha':0.5, 'pad':10})
#ax.xaxis.set_minor_formatter(FuncFormatter(ticks_format))
#for label in line.axes.get_xaxis().get_ticklabels()[::2]:
#    label.set_visible(True)
#plt.yticks(np.arange(*p_s_args))

#plt.legend(loc='lower left', fontsize='15')
ax[0].set_ylabel('Num. Columns')
ax[0].grid(True)


n_s_args = (5e5, 8.5e6, 5e5)
#p_s_args = (500, 4000, 500)
#d_s = np.linspace(5, 20, 16)

p = 2500.0
B = 32.0
k = 16.0

d = lambda n: -2.1*lambertw(((8*(1 - 4*p*B)*log(2.0))/n), 1)/log(2.0)#1e3*(D / (pow(2, D) *B))*(n/32.0) + (1/4*B)

y_s_2 = [d(n) for n in n_s_points]
#ax.fill_between(n_s_points, 0, y_s)
#ax.fill_between(n_s_points, y_s, 4000, facecolor='orange')
ax[1].plot(n_s_points, y_s_2, '-')

#plt.xticks(n_s)
ax[1].yaxis.set_major_formatter(FuncFormatter(y_ticks_format_depth))
ax[1].text(2.25e6, 3, 'Spark MLlib Better',
      bbox={'facecolor':'powderblue', 'alpha':0.5, 'pad':10})
ax[1].text(8e5, 9, 'Yggdrasil Better',
      bbox={'facecolor':'orange', 'alpha':0.5, 'pad':10})
#ax.xaxis.set_minor_formatter(FuncFormatter(ticks_format))
#for label in line.axes.get_xaxis().get_ticklabels()[::2]:
#    label.set_visible(True)
#plt.yticks(np.arange(*p_s_args))

#plt.legend(loc='lower left', fontsize='15')
ax[1].set_ylabel('Tree Depth')
ax[1].set_xlabel('Num. Rows, Log Scale')
ax[1].grid(True)
fig.subplots_adjust(hspace=0.1)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

plt.savefig('Tradeoffs.png', transparent=True, bbox_inches='tight', pad_inches=0.2, dpi=900)
