#!/usr/bin/env python

import sys
from math import sqrt

def main(argv):
    filenames = argv[1:]
    for filename in filenames:
        with open(filename, 'rb') as f:
            result_list = [float(line.split(' ')[1]) for line in f]
            print filename,
            print stats_for_results(result_list)

def average(in_list):
    return sum(in_list) / len(in_list)

def variance(in_list):
    variance = 0
    for x in in_list:
        variance = variance + (average(in_list) - x) ** 2
    return variance / len(in_list)

def stats_for_results(result_list):
    assert len(result_list) > 0, "stats_for_results given empty result_list"
    result_first = result_list[0]
    result_last = result_list[-1]
    sorted_results = sorted([float(x) for x in result_list])
    result_med = sorted_results[len(sorted_results)/2]
    if (len(result_list) % 2 == 0):
        result_med = (sorted_results[len(result_list)/2-1] + sorted_results[len(result_list)/2])/2
    result_std = sqrt(variance(sorted_results))
    result_min = sorted_results[0]

    return (result_med, result_std, result_min, result_first, result_last)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage: ./stats_for_results.py <txt files from decision-tree.out>+'
        sys.exit(1)
    main(sys.argv)
