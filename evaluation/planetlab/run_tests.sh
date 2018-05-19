#!/bin/bash

rounds=20

r=./config/readers.txt
w=./config/writers.txt
writers=$(cat $w | sort)
clients=$(cat $r $w | sort)
ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
tests=evaluation/planetlab/tests_enabled/*
test_writers=config/tests/test-writers

for step in $test_writers/*; do
  for file in $step; do
    if [[ $file = *'readers.txt' ]]; then
      r=$file
    elif [[ $file = *'writers.txt' ]]; then
      w=$file
    fi
  done
  for t in $tests; do
    if [[ $t == *'clients_write.py' ]]; then
      m=$(echo $t | sed 's/\//./g')
      module=${m%.py}
      for writer in $writers; do
        ssh -l $slice -i ~/.ssh/planetlab_rsa $writer \
          "cd ~/casss/; python3.6 -m $module 'writer' $rounds" &
      done
      for reader in $readers; do
        ssh -l $slice -i ~/.ssh/planetlab_rsa $reader \
          "cd ~/casss/; python3.6 -m $module 'reader' $rounds" &
      done
    fi
  done

  echo "Tests started!"
  wait
  echo "Tests finished!"

  echo "Fetching results..."
  mkdir -p $step
  for writer in $writers; do
    rsync -aPz -e "ssh -i $ssh_key -l $slice" $writer:~/results/* $step
  done

done

echo "All tests done!"
