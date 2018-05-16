#!/bin/bash

port=5555
servers=./config/servers.txt
defaultconf=./config/default.ini
configfile=./config/autogen.ini

n=$(wc -l $servers | cut -f 1 -d ' ')

echo "Creating configuration file"

cat $defaultconf > $configfile
echo -e "n = $n\n" >> $configfile
echo "[Nodes]" >> $configfile
i=0
while read server; do
  echo "node$i = $server:$port" >> $configfile
  i=$((i+1))
done <$servers

echo "Config file created!"
cat $configfile
