#!/bin/bash

read -n 1 -p "Remember to update config/servers.txt! Press enter to continue..."
./evaluation/planetlab/setup/create_config.sh
./evaluation/planetlab/setup/copy_to_servers.sh
./evaluation/planetlab/setup/install.sh
