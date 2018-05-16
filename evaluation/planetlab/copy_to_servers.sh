#!/bin/bash

ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
servers=./config/servers.txt

failed=0

echo "Copying working directory to servers..."

while read server; do
  rsync -aPz -e "ssh -i $ssh_key -l $slice" ./* $server:~/casss \
    && echo "Transfer to $server sucessful!"  \
    || { echo "Failed transfer to $server"; failed=1; break; }
done <$servers

if [ $failed -eq 0 ]; then
  echo "Transfer sucessful!"
else
  echo "Transfer failed!"
fi
