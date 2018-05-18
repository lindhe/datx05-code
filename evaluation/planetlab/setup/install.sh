#!/bin/bash

install_script=./evaluation/planetlab/setup/install_deps.sh
servers=$(cat ./config/servers.txt | sort | uniq)
clients=$(cat ./config/clients.txt | sort | uniq)
ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2

failed=0

for server in $servers; do
  echo "Installing system on $server..."
  ssh -i $ssh_key -l $slice $server 'bash -s' < $install_script \
    && echo "Installation on $server sucessful!"  \
    || { echo "Installation on $server"; failed=1; break; }
done

if [ $failed -eq 0 ]; then
  for client in $clients; do
    echo "Installing system on $client..."
    ssh -i $ssh_key -l $slice $client 'bash -s' < $install_script \
      && echo "Installation on $client sucessful!"  \
      || { echo "Installation on $client"; failed=1; break; }
  done
fi

if [ $failed -eq 0 ]; then
  echo "Installation sucessful!"
else
  echo "Installation failed!"
fi
