#!/usr/bin/env python

from utils import save_figure, add_legend
import matplotlib.pyplot as plt
import config
import re
import glob

DEBUG = False

DIRS = {
 'by-feature': [(1, 7, 'Yggdrasil vs. PLANET: Number of Features')],
 'mnist-8m': [(4, 7, 'Yggdrasil vs. MLlib and XGBoost: MNIST 8M')],
 'yahoo': [(4, 7, 'Yggdrasil vs. MLlib and XGBoost: Yahoo 2M')],
#'friedman-1': [(4, 8, 'Friedman 1 Generator: Train RMSE'),
#(4, 9, 'Friedman 1 Generator: Test RMSE')],
#'year-prediction-msd': [(4, 8, 'YearPredictionMSD Train RMSE'),
#(4, 9, 'YearPredictionMSD Test RMSE')],
}

MARKERS = {
  'byRow*.tsv': 'x',
  'byCol*.tsv': '.',
  'xgboost.tsv': '*',
}

LABELS_COLORS = {
  'tsvs/mnist-8m/byRow.tsv': ('MLlib', 'b'),
  'tsvs/mnist-8m/byCol2.tsv': ('Yggdrasil', 'g'),
  'tsvs/mnist-8m/xgboost.tsv': ('XGBoost', 'r'),
  'tsvs/yahoo/byRow.tsv': ('MLlib', 'b'),
  'tsvs/yahoo/byCol2.tsv': ('Yggdrasil', 'g'),
  'tsvs/yahoo/xgboost.tsv': ('XGBoost', 'r'),
  'tsvs/by-feature/byRow15.tsv': ('MLlib, D = 15', 'b'),
  'tsvs/by-feature/byRow16.tsv': ('MLlib, D = 13', 'orangered'),
  'tsvs/by-feature/byCol15.tsv': ('Yggdrasil, D = 15', 'g'),
  'tsvs/by-feature/byCol16.tsv': ('Yggdrasil, D = 13', 'goldenrod')
}

if __name__ == '__main__':
    for dir, plot_infos in DIRS.items():
        if DEBUG: print dir
        for (x_val_index, y_val_index, title) in plot_infos:
            if DEBUG: print title
            plt.figure()
            for glob_pattern, marker in MARKERS.items():
                for full_path in glob.iglob('tsvs/' + dir + '/' + glob_pattern):
                    if DEBUG: print full_path
                    with open(full_path) as f:
                        header = f.readline()
                        header_vals = header.strip().split('\t')
                        x_label = header_vals[x_val_index]
                        y_label = header_vals[y_val_index]
                        xs, ys = [], []
                        for line in f:
                            if line[0] == '#':
                                continue
                            vals = line.strip().split('\t')
                            if DEBUG: print vals
                            x_val = int(vals[x_val_index])
                            y_val = float(vals[y_val_index])
                            xs.append(x_val)
                            ys.append(y_val)
                        label, color = LABELS_COLORS[full_path] if full_path in LABELS_COLORS \
                                                                else (full_path[len('tsvs/' + dir + '/'):-4], None)
                        plt.plot(xs, ys, marker + '-', label=label, color=color)
                        plt.xlabel(x_label)
                        plt.ylabel(y_label)
            if dir == 'mnist-8m':
                plt.ylim([0, 2500])
                plt.xlim([5, 20])
            elif dir == 'yahoo':
                plt.ylim([0, 10000])
                plt.xlim([5, 18])
            add_legend('upper left')
            plt.grid(True)
            save_figure(dir, title)

