#!/bin/bash
# Checks if node is server. If it is, it starts the server program.
# Otherwise, it starts the Client application prompt.

address=$(hostname)
slice=chalmersple_casss2
config=./casss/config/autogen.ini

# For each time my address is in autogen.ini, start a server
servers=$(grep $address $config | cut -d ' ' -f 3)

for server in $servers; do
  address=$(echo $server | cut -d ':' -f 1)
  port=$(echo $server | cut -d ':' -f 2)
  echo "Starting server at $address:$port"
  sudo python3.6 /home/$slice/casss/server.py $port $address $config > /dev/null &
done
