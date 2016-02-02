#!/usr/bin/env python

import matplotlib.pyplot as plt
import re
import glob

DEBUG = False

DIRS = {
        'by-feature': [(1, 7, 'By Feature')],
        'mnist-8m': [(4, 7, 'MNIST 8M')],
        'internet-web-company': [(4, 7, 'Large-Scale Web Company')],
        'friedman-1': [(4, 8, 'Friedman 1 Generator: Train RMSE'),
                       (4, 9, 'Friedman 1 Generator: Test RMSE')],
        'year-prediction-msd': [(4, 8, 'YearPredictionMSD Train RMSE'),
                                (4, 9, 'YearPredictionMSD Test RMSE')],
        }
FILE_PATTERNS = {
                 'byRow*.tsv': 'x',
                 'byCol*.tsv': '.',
                }

plt.rc('text', usetex = True)

for dir, plot_infos in DIRS.items():
    if DEBUG: print dir
    for (x_val_index, y_val_index, title) in plot_infos:
        if DEBUG: print title
        plt.figure()
        for glob_pattern, marker in FILE_PATTERNS.items():
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
                    plt.plot(xs, ys, marker + '-', label = full_path[len('tsvs/' + dir + '/'):-4])
                    plt.xlabel(x_label)
                    plt.ylabel(y_label)
        plt.legend(loc='best', ncol=2)
        plt.title(title)
        plt.grid(True)
        filename = re.sub(r'(:|\s+)', '_', title)
        plt.savefig(filename + '.eps')

