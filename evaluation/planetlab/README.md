# PlanetLab Testbed Scripts

All scripts in this directory must be run from the root of this repository.

## Workflow

0. Make sure your working directory is the root of this repository.
1. Create a slice on PlanetLab, assign it to user(s) and add servers to it.
2. Populate `config/servers.txt` and `config/clients.txt` respectively. Duplicate lines will install duplicate instances.
3. Make sure the correct tests are symlinked to evaluation/planetlab/tests-enabled/
4. Install and start service.
5. Run tests.
6. Cleanup.

### Installation

```
$ evaluation/planetlab/install_system.sh
$ evaluation/planetlab/servers_start.sh
```

### Tests

```
$ python3.6 -m evaluation.planetlab.servers_init
$ evaluation/planetlab/run_tests.sh
```

### Cleanup

```
$ evaluation/planetlab/servers_teardown.sh
```
