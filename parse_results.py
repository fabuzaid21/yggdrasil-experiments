#!/usr/bin/env python

import re
import sys
import os

PARAMS_REGEX = r'--num-examples=(\d+)\s--num-features=(\d+)\s--label-type=(\d+).*--tree-depth=(\d+).*--alg-type=(\w+).*--training-data=(\S*)\s--test-data=(\S*)\s'
TRAIN_TIME_REGEX = r'Training time: (\d+\.\d+)'
TRAIN_METRIC_REGEX = r'Training Set Metric: (\d+\.\d+)'
TEST_METRIC_REGEX = r'Test Set Metric: (\d+\.\d+)'

DELIMITER='\t'
HEADER_VALS = ['Rows', 'Columns', 'Train Data', 'Test Data', 'Depth', 'Algo', 'Label', 'Training Time (s)', 'Training Metric', 'Test Metric']
TSV_HEADER = DELIMITER.join(HEADER_VALS) + '\n'
TSV_DIR = 'tsvs/'

def main(argv):
    filenames = argv[1:]
    if not os.path.exists(TSV_DIR):
        os.makedirs(TSV_DIR)
    for filename in filenames:
        tsv_filename = os.path.splitext(filename)[0] + '.tsv'
        tsv_file = open(TSV_DIR + tsv_filename, 'w')
        tsv_file.write(TSV_HEADER)
        with open(filename, 'rb') as f:
            while True:
                line = f.readline()
                if not line: break

                m = re.search(PARAMS_REGEX, line)
                num_examples, num_features,\
                label_type, tree_depth,\
                alg_type, train_data,\
                test_data = m.group(1, 2, 3, 4, 5, 6, 7)
                if (label_type == '0'):
                    label_type = 'Regression'
                else:
                    label_type = 'Classification: ' + label_type

                line = f.readline()
                m = re.search(TRAIN_TIME_REGEX, line)
                train_time = m.group(1)

                f.readline() # consume the "Test Time" line

                line = f.readline()
                m = re.search(TRAIN_METRIC_REGEX, line)
                train_set_metric = m.group(1)

                line = f.readline()
                m = re.search(TEST_METRIC_REGEX, line)
                test_set_metric = m.group(1)

                if train_data is None:
                    train_data = ''
                else:
                    train_data = re.sub(r'^hdfs.*9000\/', '', train_data)
                if test_data is None:
                    test_data = ''
                else:
                    test_data = re.sub(r'^hdfs.*9000\/', '', test_data)

                result_line = [num_examples, num_features, train_data,\
                               test_data, tree_depth, alg_type, label_type,\
                               train_time, train_set_metric, test_set_metric]

                tsv_file.write(DELIMITER.join(result_line) + '\n')
        tsv_file.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage: ./parse_results.py <spark_perf_output_file>+'
        sys.exit(1)
    main(sys.argv)
