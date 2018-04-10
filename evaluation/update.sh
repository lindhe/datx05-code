#!/bin/bash

if [ $# -eq 0 ]; then
    n=5
else
    n=$1
fi

# Update files
echo "Updating files..."
for i in $( seq 0 $n ); do
    docker cp . "c$i:/opt/project"
done;


