#!/bin/bash

opts="StrictHostKeyChecking=no"
s=./config/servers.txt
c=./config/clients.txt
all=$(cat $s $c | sort | uniq)
ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
failed=0

echo "Removing __pycache__ files..."
find . -path "**/__pycache__/*" -delete
echo "Copying working directory to servers..."

for server in $all; do
  rsync -rlptoPz --delete -e "ssh -o $opts -i $ssh_key -l $slice" ./* $server:~/casss \
    && echo "Transfer to $server sucessful!"  \
    || { echo "Failed transfer to $server"; failed=1; break; }
done

if [ $failed -eq 0 ]; then
  echo "Transfer sucessful!"
else
  echo "Transfer failed!"
fi
