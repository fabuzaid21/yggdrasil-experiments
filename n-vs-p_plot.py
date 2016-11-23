#!/usr/bin/env python

from utils import save_figure
from matplotlib.ticker import FuncFormatter
from math import pow
import matplotlib.pyplot as plt
import config
import numpy as np

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
      return '$p$'
    return '${0:d}p$'.format(index)

n_s_args = (5e5, 8.5e6, 5e5)
p_s_args = (500, 4000, 500)

D = 15.0
B = 32.0
k = 16.0

if __name__ == '__main__':
    p = lambda n: 1e3*(D / (pow(2, D) *B))*(n/32.0) + (1/4*B)

    n_s_points = np.linspace(*n_s_args)
    y_s = [p(n) for n in n_s_points]
    fig, ax = plt.subplots()
    ax.plot(n_s_points, y_s, '-')

    ax.set_xscale('log')
    ax.set_xlim([n_s_args[0], n_s_args[1]])
    ax.set_xticks(np.arange(*n_s_args))
    ax.xaxis.set_major_formatter(FuncFormatter(x_ticks_format))
    ax.yaxis.set_major_formatter(FuncFormatter(y_ticks_format))
    ax.text(2.5e6, 350, 'PLANET Better',
          bbox={'facecolor':'powderblue', 'alpha':0.5, 'pad':10})
    ax.text(8e5, 2700, 'Yggdrasil Better',
          bbox={'facecolor':'orange', 'alpha':0.5, 'pad':10})

    plt.ylabel('Num. Features')
    plt.xlabel('Num. Instances, Log Scale')
    plt.grid(True)
    save_figure('n-vs-p', 'Num. Instances vs. Num. Features')

