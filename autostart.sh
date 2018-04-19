#!/bin/bash
# Checks if node is server. If it is, it starts the server program.
# Otherwise, it starts the Client application prompt.

port=5555
ip=$(hostname -I | awk '{$1=$1}1')
config=/opt/project/config/autogen.ini

# Check if my IP is in autogen.ini
# If my IP is in the list, I'm a server.
grep -c $ip $config > /dev/null

if [ $? -eq 0 ]; then
  echo "Starting Server..."
  python3.6 /opt/project/server.py $port $ip $config
else
  echo "Starting Client..."
  sleep 1
  python3.6 -O /opt/project/run_client.py $config
fi

