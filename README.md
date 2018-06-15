**Authors:**

Robert Gustafsson <robg@student.chalmers.se>

Andreas Lindhé <andreas@lindhe.io>

# Self-Stabilizing Services for Emulating Distributed Shared Memory on Message Passing Platforms

This is the outcome of our master's thesis project, during the spring of 2018.
We are the first ones to implement and practically evaluate the self-stabilizing
version of _Coded Atomic Storage_ (CAS) by
[Dolev, Petig and Schiller](https://arxiv.org/abs/1806.03498).

## License

This project is licensed under the MIT license.
Please see the LICENSE file.
The copyright belongs to the authors.

## Installation

The project was exclusively developed on and for Linux, but might run on other
system too.
If you find important points for a specific platform, please tell us.

### Dependencies

* `bash`
* `python3.6`
* `liberasurecode`
* `docker`
* `rsync`
* `ssh`

**Install required python modules:**
```
$ pip3.6 install -r requirements.txt
```

### Needed for the CAS_ZMQ version:

* `python3.6`
* `zeromq`
* `pyzmq`

## Repository Structure

There is a method to our madness, at least sometimes.
It would be good to clean up things more, but this is a brief overview of what's
where in this repository.
More detailed README files are found in each of the subdirectories, but this is
the gists of it:

### Code

**Terms:**
* CASSS is the self-stabilizing version of CAS
* CAS\_ZMQ is an implementation of CAS which does not use any self-stabilizing techniques
* AR stands for Atomic Register
* Atomic Register is an incorrect name for the SIMPLE algorithm by Georgiou
* SIMPLE is a MWMR version of ABD

#### Directories
* `atomic_regsiter/`: code for the SIMPLE algorithm (MWMR ABD)
* `cas/`: code for CAS and CASSS algorithms
* `channel/`: code for the self-stabilizing communication channel
* `gossip/`: code for the self-stabilizing gossiping service
* `quorum/`: code for the self-stabilizing quorum system
* `register/`: code for the module which handles storage in CAS

#### Files
* `ARclient.py`: a class implementing the SIMPLE algorithm's client protocol
* `ARserver.py`: a class implementing the SIMPLE algorithm's server protocol
* `autostart.sh`: bootstrap script for starting SIMPLE server on PlanetLab
* `cas_zmq_autostart.sh`: bootstrap script for starting CAS\_ZMQ server on PlanetLab
* `client.py`: a class implementing the CASSS algorithm's client protocol
* `server.py`: a class implementing the CASSS algorithm's server protocol
* `run_client.py`: an application running an instance of a CASSS client
* `start_multiple_servers.py`: an application spinning up multiple local instances of the CASSS server
* `start_cas_zmq_servers.py`:  an application spinning up multiple local instances of the CAS_ZMQ server

### Configuration, tests, evaluation, misc.

#### Directories
* `config/`: is meant to hold configuration files and related scripts.
  But accidentally, it also includes a lot of other things, mainly related to
  evaluation and debugging.
* `evaluation/`: scripts for evaluation
* `test/`: test to find out if basic functionality of the system works

#### Files
* `Dockerfile`: configuration file used for test bed (and potentially deployment)
* `requirements.py`: required dependencies for pip (and/or Docker) to install

### Usage

#### Locally

#### Test Bed

#### Evaluation Platform

### Code Style

* Line width: 80 characters
* Indentation: 2 spaces
* Use verbose variable names whenever possible
* All filenames and module names should be in `snake_case`.
* All class names should be in `CamelCase`.
* Documentation should be in
  [Google Style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
* All scripts should start with a `#!` defining the interpretor to use (e.g.,
  `#!/bin/python3.6`)
* Try to keep commits atomic
* Use roughly [this Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
