#!/usr/bin/env python

import matplotlib.pyplot as plt

DIRS = {
        'by-feature': (1, 8),
        #'by-instance': 0,
        #'by-tree-depth': 4,
        'mnist-8m': (4, 7),
        'internet-web-company': (4, 7)
        }
FILES = ['byRow.tsv', 'byCol.tsv']


plt.rc('text', usetex = True)

for dir, (x_val_index, y_val_index) in DIRS.items():
    plt.figure()
    for file in FILES:
        with open('tsvs/' + dir + '/' + file) as f:
            header = f.readline()
            x_label = header.split('\t')[x_val_index]
            xs, ys = [], []
            for line in f:
                if line[0] == '#':
                    continue
                vals = line.split('\t')
                x_val = int(vals[x_val_index])
                y_val = float(vals[y_val_index])
                # num_instances, num_features, train_data, test_data, depth, algo,\
                # label, training_time, training_metric, test_metric\
                # = int(vals[0]), int(vals[1]), vals[2], vals[3], int(vals[4]), vals[5],\
                # vals[6], float(vals[7]), float(vals[8]), float(vals[9])
                xs.append(x_val)
                ys.append(y_val)
            plt.plot(xs, ys, '.-', label = file[:-4])
            plt.ylabel('Training Time (s)')
            plt.xlabel(x_label)
    plt.legend(loc='upper left')
    plt.title(dir)
    plt.grid(True)
    plt.savefig(dir + '.eps')

