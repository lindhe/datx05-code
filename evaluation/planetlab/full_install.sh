#!/bin/bash

echo "Remember to update config/servers.txt!"
./evaluation/planetlab/create_config.sh
./evaluation/planetlab/copy_to_servers.sh
./evaluation/planetlab/install.sh
