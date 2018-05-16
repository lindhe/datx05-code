#!/bin/bash

install_script=./evaluation/planetlab/install_deps.sh
servers=./config/servers.txt
ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2

failed=0

while read server; do
  echo "Installing system on $server..."
  ssh -i $ssh_key -l $slice $server 'bash -s' < $install_script \
    && echo "Installation on $server sucessful!"  \
    || { echo "Installation on $server"; failed=1; break; }
done <$servers

if [ $failed -eq 0 ]; then
  echo "Installation sucessful!"
else
  echo "Installation failed!"
fi
