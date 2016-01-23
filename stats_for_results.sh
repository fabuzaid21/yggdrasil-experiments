#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "One argument required: [decision-tree.out file]"
    exit 1
fi

grep trainingTime $1 > trainingTime.txt
grep trainingMetric $1 > trainingMetric.txt
grep testMetric $1 > testMetric.txt

./stats_for_results.py trainingTime.txt trainingMetric.txt testMetric.txt
rm -f trainingTime.txt trainingMetric.txt testMetric.txt
