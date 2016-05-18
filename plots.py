#!/usr/bin/env python

import matplotlib.pyplot as plt
import re
import glob

DEBUG = False

DIRS = {
#'by-feature': [(1, 7, 'Yggdrasil vs. PLANET: Number of Features')],
  'mnist-8m': [(4, 7, 'Yggdrasil vs. PLANET: MNIST 8M')],
  'internet-web-company': [(4, 7, 'Yggdrasil vs. PLANET: Leading Web Company')],
#'friedman-1': [(4, 8, 'Friedman 1 Generator: Train RMSE'),
#(4, 9, 'Friedman 1 Generator: Test RMSE')],
#'year-prediction-msd': [(4, 8, 'YearPredictionMSD Train RMSE'),
#(4, 9, 'YearPredictionMSD Test RMSE')],
}
MARKERS = {
  'byRow*.tsv': 'x',
  'byCol*.tsv': '.',
}
LABELS_COLORS = {
  'tsvs/mnist-8m/byRow2.tsv': ('PLANET', 'b'),
  'tsvs/mnist-8m/byCol2.tsv': ('Yggdrasil', 'g'),
  'tsvs/internet-web-company/byRow.tsv': ('PLANET', 'b'),
  'tsvs/internet-web-company/byCol.tsv': ('Yggdrasil', 'g'),
  'tsvs/by-feature/byRow15.tsv': ('PLANET, D = 15', 'b'),
  'tsvs/by-feature/byRow5.tsv': ('PLANET, D = 5', 'cyan'),
  'tsvs/by-feature/byCol15.tsv': ('Yggdrasil, D = 15', 'g'),
  'tsvs/by-feature/byCol5.tsv': ('Yggdrasil, D = 5', 'magenta')
}

plt.rc('text', usetex = True)
plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plt.rcParams.update({'font.size': 18})
# TODO:
# Get current size
# fig_size = plt.rcParams["figure.figsize"]
# Set figure width to 12 and height to 6 (originally, 8 & 6)
# fig_size[0] = 12
# fig_size[1] = 6
# plt.rcParams["figure.figsize"] = fig_size


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
                        # num_instances, num_features, train_data,\
                        # test_data, depth, algo,\
                        # label, training_time, training_metric, test_metric\
                        # = int(vals[0]), int(vals[1]), vals[2], vals[3],\
                        # int(vals[4]),vals[5],\
                        # vals[6], float(vals[7]), float(vals[8]), float(vals[9])
                        xs.append(x_val)
                        ys.append(y_val)
                    label, color = LABELS_COLORS[full_path] if full_path in LABELS_COLORS \
                                                            else (full_path[len('tsvs/' + dir + '/'):-4], None)
                    plt.plot(xs, ys, marker + '-', markersize=10, label=label, color=color)
                    plt.xlabel(x_label)
                    plt.ylabel(y_label)
        if dir == 'mnist-8m':
            plt.ylim([0, 2500])
        plt.legend(loc='upper left', fontsize='17')
        plt.title(title)
        plt.grid(True)
        filename = re.sub(r'(:|\s+)', '_', title)
        plt.savefig(filename + '.eps')

