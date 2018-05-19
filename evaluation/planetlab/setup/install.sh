#!/bin/bash

s=./config/servers.txt
r=./config/readers.txt
w=./config/writers.txt
all=$(cat $s $r $w | sort | uniq)
install_script=./evaluation/planetlab/setup/install_deps.sh
ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2

failed=0

for server in $all; do
  echo "Installing system on $server..."
  ssh -i $ssh_key -l $slice $server 'bash -s' < $install_script \
    && echo "Installation on $server sucessful!"  \
    || { echo "Installation on $server"; failed=1; break; }
done

if [ $failed -eq 0 ]; then
  echo "Installation sucessful!"
else
  echo "Installation failed!"
fi
