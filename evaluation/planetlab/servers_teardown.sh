#!/bin/bash

servers=$(cat ./config/servers.txt | sort | uniq)

echo "Killing servers"

for server in $servers; do
  ssh -l chalmersple_casss2 -i ~/.ssh/planetlab_rsa $server \
    "sudo pkill -9 python3.6; sudo find ~ -path '*/.storage*' -delete"
done

echo "DONE"
