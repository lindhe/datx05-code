#!/bin/bash

rounds=20

opts="StrictHostKeyChecking=no"
ssh_key=~/.ssh/planetlab_rsa
slice=chalmersple_casss2
tests=evaluation/planetlab/tests_enabled/*
test_writers=config/tests/test-writers
config="/home/$slice/casss/config/autogen.ini"

for step in $test_writers/*; do
  scenario=$(echo "$step" | sed 's/.*\/\(step.*\)/\1/')

  for file in $step/*; do
    if [[ $file = *'readers.txt' ]]; then
      r=$file
      readers=$(cat $r | sort)
    elif [[ $file = *'writers.txt' ]]; then
      w=$file
      writers=$(cat $w | sort)
    fi
  done

  for t in $tests; do
    if [[ $t == *'clients_write.py' ]]; then
      m=$(echo $t | sed 's/\//./g')
      module=${m%.py}
      for writer in $writers; do
        ssh -o $opts -l $slice -i ~/.ssh/planetlab_rsa $writer \
          "cd ~/casss/; python3.6 -m $module 'writer' $rounds $config $step" &
      done
      for reader in $readers; do
        ssh -o $opts -l $slice -i ~/.ssh/planetlab_rsa $reader \
          "cd ~/casss/; python3.6 -m $module 'reader' $rounds $config" &
      done
    fi
  done

  echo "Tests started!"
  wait
  echo "Tests finished!"

  echo "Fetching results..."
  mkdir -p $step
  for writer in $writers; do
    rsync -aPz -e "ssh -o $opts -i $ssh_key -l $slice"\
      $writer:~/results/$scenario* $step
  done

  python3.6 -m evaluation.planetlab.summary $step

done

echo "All tests done!"
