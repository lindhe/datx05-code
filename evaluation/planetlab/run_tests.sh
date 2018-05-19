#!/bin/bash

rounds=20

ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
clients=$(cat ./config/clients.txt | sort)
tests=evaluation/planetlab/tests_enabled/*

for t in $tests; do
  if [[ $t != *'__init__.py' ]]; then
    m=$(echo $t | sed 's/\//./g')
    module=${m%.py}
    for client in $clients; do
      ssh -l $slice -i ~/.ssh/planetlab_rsa $client \
        "cd ~/casss/; python3.6 -m $module $rounds" &
    done
  fi
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
