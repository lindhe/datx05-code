# PlanetLab Testbed Scripts

All scripts in this directory must be run from the root of this repository.

## Workflow

0. Make sure your working directory is the root of this repository.
1. Create a slice on PlanetLab, assign it to user(s) and add servers to it.
2. Populate `config/servers.txt` and `config/clients.txt` respectively. Duplicate lines will install duplicate instances.
3. Install and start service.
4. Run tests.
5. Cleanup.

### Installation

```
$ evaluation/planetlab/install_system.sh
$ evaluation/planetlab/servers_start.sh
```

### Tests

```
$ ./servers_init.py
$ evaluation/planetlab/tests/test_1.sh; # etc.
```

### Cleanup

```
$ evaluation/planetlab/servers_teardown.sh
```
