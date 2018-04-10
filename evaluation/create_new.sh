#!/bin/bash

if [ $# -eq 0 ]; then
    n=5
else
    n=$1
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
        --mount src=/srv/casss/,dst=/storage/,type=bind \
        casss_server;
done;

# # Install iperf3 on two nodes
# echo "Installing iperf3 on two nodes..."
# for i in {1..2}; do
#     docker network connect bridge c$i;
#     docker exec -it c$i ash -c "apk update && apk add iperf3";
#     docker network disconnect bridge c$i;
# done;
# echo "Installation done"

