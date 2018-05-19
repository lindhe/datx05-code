#!/bin/python3.6
# -*- coding: utf-8 -*-
#
# License: MIT

import sys
import os
import pathlib
import configparser
import re
from pathlib import Path

def main(rel_path):
    res_path = os.getcwd() + '/' + rel_path + '/'
    res_file = res_path + "summary.txt"

    results = configparser.ConfigParser()
    files = os.listdir(res_path)
    regex = re.compile('.*log')
    filtered_files = [x for x in files if regex.match(x)]
    avg = []
    avg_no_outliers = []
    for f in filtered_files:
        results.read(res_path + f)
        avg.append(float(results['Average']['average']))
        avg_no_outliers.append(float(results['Average']['average_no_outliers']))
        test = results['Meta']['test']
        rounds = results['Meta']['rounds']
        outliers = results['Meta']['outliers']

    summary = sum(avg)/len(avg)
    summary_no_outliers = sum(avg_no_outliers)/len(avg_no_outliers)
    result = f"Average from {len(avg)} {test} clients during {rounds} rounds:\nAll: {summary}\nRemoved {outliers} outliers: {summary_no_outliers}"
    with open(res_file, 'a') as f:
        f.write(result)
    print(f"Created summary file {res_file}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        raise Exception("Missing argument: relative path")
    main(path)
