#!/bin/bash

echo "Remember to update config/servers.txt!"
./evaluation/planetlab/setup/create_config.sh
./evaluation/planetlab/setup/copy_to_servers.sh
./evaluation/planetlab/setup/install.sh
