#!/bin/bash

ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
clients=$(cat ./config/clients.txt | sort)
tests=./evaluation/planetlab/tests-enabled/*

for t in $tests; do
  for client in $clients; do
    ssh -l $slice -i ~/.ssh/planetlab_rsa $client "bash -s" < $t &
  done
done

echo "All tests started!"
wait
echo "All tests finished!"

echo "Fetching results..."
res=./results/$(date +'%F_%T')
mkdir -p $res
for client in $clients; do
  rsync -aPz -e "ssh -i $ssh_key -l $slice" $client:~/results/* $res
done
echo "Check out the results in $res"
