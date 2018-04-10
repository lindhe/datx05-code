FROM ubuntu:latest
LABEL Description="Docker image for CASSS servers"

ADD . /opt/project
WORKDIR /opt/project

# Install base system required for build
RUN apt-get update &&\
    apt-get install -y \
    gcc g++ musl-dev bash \
    python3-dev python3-pip &&\
    pip3 install --upgrade pip

# Install dependencies
RUN apt-get install -y libzmq-dev liberasurecode-dev
RUN pip3 install -r requirements.txt

EXPOSE 5555

# CMD ["python","-u", "server.py"]
