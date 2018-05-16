#!/bin/bash

ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
servers=./config/servers.txt

while read server; do
  ssh -l chalmersple_casss2 -i ~/.ssh/planetlab_rsa \
    && echo "Running server on $server"  \
    || { echo "Failed on $server"; failed=1; break; }
done <$servers


if [ $failed -eq 0 ]; then
  echo "Service is running"
else
  echo "Service down"
fi
