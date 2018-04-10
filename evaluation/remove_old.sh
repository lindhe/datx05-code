#!/bin/bash

if [ $# -eq 0 ]; then
    n=5
else
    n=$1
fi

# 0. Remove old setup
echo "Removing old setup..."
for i in $( seq 0 $n ); do
    docker container stop "c$i"
    docker container rm "/c$i"
    sudo tunctl -d tap-$i
done;
docker network prune -f
echo "Removed all old containers, bridges and taps!"

