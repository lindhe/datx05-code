#!/bin/bash

if [ $# -eq 0 ]; then
    nodes=4
else
    nodes=$1
fi

resfile=perf_result.txt
echo "Result of test with $nodes nodes at $(date +'%F_%T')" >> $resfile
echo "==================================================" >> $resfile

echo "Setting up test environment..."
/home/andreas/thesis-code/evaluation/create_new.sh $nodes

n=$(grep -E "^n =" ~/thesis-code/config/autogen.ini | cut -f 3 -d ' ')
n=$(((n+1)/2))

echo "Please start NS-3!"
read -p "Press enter after you have started NS-3:"
echo ""

ips=$(tail -n $n ~/thesis-code/config/autogen.ini |\
  cut -d ' ' -f 3 |\
  cut -d ':' -f 1)

i=$n
for ip in $ips; do
  docker exec c$i iperf3 -sD
  i=$((i+1))
done

i=0
for ip in $ips; do
  docker exec c$i iperf3 -c $ip | grep -E "sender|receiver" | tee -a $resfile &
  i=$((i+1))
done

wait;
echo "" >> $resfile

echo "Please stop NS-3!"
read -p "Press enter after you have stopped NS-3:"
echo ""

echo "Tear down test environment..."
~/thesis-code/evaluation/remove_old.sh $nodes
