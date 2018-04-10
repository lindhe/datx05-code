FROM ubuntu:16.04
LABEL Description="Docker image for CASSS servers"

COPY . /opt/project
WORKDIR /opt/project


# Install base system required for build
RUN apt-get update &&\
    apt-get install -y \
    gcc g++ musl-dev bash software-properties-common \
    curl

# Install python3.6
RUN add-apt-repository ppa:deadsnakes/ppa &&\
    apt-get update &&\
    apt-get install -y \
    python3.6-dev &&\
    curl https://bootstrap.pypa.io/get-pip.py | python3.6

# Install dependencies
RUN apt-get install -y libzmq-dev \
    liberasurecode-dev libjerasure-dev
RUN pip3 install -r requirements.txt

EXPOSE 5555
