#!/bin/bash
# Checks if node is server. If it is, it starts the server program.
# Otherwise, it starts the Client application prompt.

port=5555
address=$(hostname)
slice=chalmersple_casss2
config=/home/$slice/casss/config/autogen.ini

# Check if my address is in autogen.ini
# If my address is in the list, I'm a server.
grep -c $address $config > /dev/null

if [ $? -eq 0 ]; then
  echo "Starting Server..."
  sudo python3.6 /home/$slice/casss/server.py $port $address $config
else
  echo "Starting Client..."
  sleep 1
  sudo python3.6 -O /home/$slice/casss/run_client.py $config
fi

