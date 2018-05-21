#!/bin/bash

opts="StrictHostKeyChecking=no"
slice=chalmersple_casss2
clients=$(cat ./config/readers.txt ./config/writers.txt | sort | uniq)

echo "Removing clients results directory"

for client in $clients; do
  ssh -o $opts -l $slice -i ~/.ssh/planetlab_rsa $client \
    "rm -r ~/results/*"
done

echo "DONE"
