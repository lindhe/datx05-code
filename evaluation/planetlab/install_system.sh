#!/bin/bash

read -n 1 -p "Remember to update servers.txt, readers.txt and writers.txt! Press enter to continue..."
./evaluation/planetlab/setup/create_config.sh
./evaluation/planetlab/setup/copy_to_planetlab.sh
./evaluation/planetlab/setup/install.sh
