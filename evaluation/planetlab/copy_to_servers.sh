#!/bin/bash

ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
servers=$(cat ./config/servers.txt | sort | uniq)
failed=0

echo "Copying working directory to servers..."

for server in $servers; do
  rsync -aPz -e "ssh -i $ssh_key -l $slice" ./* $server:~/casss \
    && echo "Transfer to $server sucessful!"  \
    || { echo "Failed transfer to $server"; failed=1; break; }
done

if [ $failed -eq 0 ]; then
  echo "Transfer sucessful!"
else
  echo "Transfer failed!"
fi