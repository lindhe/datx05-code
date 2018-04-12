#!/bin/bash

if [ $# -eq 0 ]; then
    n=4
else
    n=$(($1-1))
fi

# 1. Create new taps
echo "Recreating taps..."
for i in $( seq 0 $n ); do
    sudo tunctl -d tap-$i
    sudo tunctl -t tap-$i
    sudo ifconfig tap-$i 0.0.0.0 promisc up
done;
echo "The taps are opened!!!"


# 2. Create tapXnet
echo "Creating macvlan's..."
for i in $( seq 0 $n ); do
    docker network create -d macvlan \
        --subnet=172.16.86.0/24 \
        -o parent="tap-$i" "tap-$i-net";
done;
echo "Created macvlan's!"


# 3. Run nodes with alipne ash on bridge
echo "Creating new containers..."
for i in $( seq 0 $n ); do
    docker run -dit \
        --name "c$i" \
        --network="tap-$i-net" \
        --mount src=storage,dst=/storage/ \
        casss_server;
done;

# Update files
echo "Updating files..."
for i in $( seq 0 $n ); do
    docker cp . "c$i:/opt/project"
done;
