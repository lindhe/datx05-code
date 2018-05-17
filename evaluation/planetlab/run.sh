#!/bin/bash

ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
servers=$(cat ./config/servers.txt | sort | uniq)
failed=0

for server in $servers; do
  ssh -l chalmersple_casss2 -i ~/.ssh/planetlab_rsa $server "~/casss/autostart.sh" \
    && echo "Running server on $server"  \
    || { echo "Failed on $server"; failed=1; break; }
done


if [ $failed -eq 0 ]; then
  echo "Service is running"
else
  echo "Service down"
fi
