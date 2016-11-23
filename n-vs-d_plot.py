#!/usr/bin/env python

import matplotlib.pyplot as plt
import config
from matplotlib.ticker import FuncFormatter
import numpy as np
from math import log
from scipy.special import lambertw

"""
Converts to labels to scientific notation: n*e^m
To have all the number of the same size they are all returned as latex
strings
"""
def x_ticks_format(value, index):
    exp = np.floor(np.log10(value))
    base = value/10**exp
    if not(index == 1 or index == 4 or index == 7 or index == 15):
      return ''
    if index == 1:
      return '$n$'
    return '${0:d}n$'.format(int(base))

"""
Converts to labels to scientific notation: n*e^m
To have all the number of the same size they are all returned as latex
strings
"""
def y_ticks_format(value, index):
    if index == 0:
      return ''
    if index == 1:
      return '$D$'
    return '${0:d}D$'.format(index)

n_s_args = (5e5, 8.5e6, 5e5)

p = 2500.0
B = 32.0
k = 16.0

if __name__ == '__main__':
    d = lambda n: -2.1*lambertw(((8*(1 - 4*p*B)*log(2.0))/n), 1)/log(2.0)#1e3*(D / (pow(2, D) *B))*(n/32.0) + (1/4*B)

    n_s_points = np.linspace(*n_s_args)
    y_s = [d(n) for n in n_s_points]
    fig, ax = plt.subplots()
    ax.plot(n_s_points, y_s, '-')

    ax.set_xscale('log')
    ax.set_xlim([n_s_args[0], n_s_args[1]])
    ax.set_xticks(np.arange(*n_s_args))
    ax.xaxis.set_major_formatter(FuncFormatter(x_ticks_format))
    ax.yaxis.set_major_formatter(FuncFormatter(y_ticks_format))
    ax.text(2.5e6, 3, 'PLANET Better',
          bbox={'facecolor':'powderblue', 'alpha':0.5, 'pad':10})
    ax.text(8e5, 9, 'Yggdrasil Better',
          bbox={'facecolor':'orange', 'alpha':0.5, 'pad':10})

    plt.title('Num. Instances vs. Max Tree Depth', y=1.04)
    plt.ylabel('Tree Depth')
    plt.xlabel('Num. Instances, Log Scale')
    plt.grid(True)
    plt.savefig('n-vs-d.svg', transparent=True, pad_inches=2.5)

