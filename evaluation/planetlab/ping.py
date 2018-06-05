#!/bin/env python3.6

import sys
import os

path = sys.argv[1]
addr_list = []
with open(path) as f:
    addr_list = f.read().splitlines()
avg_list = []
for addr in addr_list:
    response = os.popen("ping -c 10 "+addr+" | tail -1 | awk '{print $4}' | cut -d '/' -f 2").read()
    avg_list.append(float(response))
max_val = max(avg_list)
min_val = min(avg_list)
avg_val = sum(avg_list)/float(len(avg_list))
print(f"min\t& max\t& avg")
print(f"{min_val}\t& {max_val}\t& {avg_val}")
