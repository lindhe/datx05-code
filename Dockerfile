FROM alpine:latest
LABEL Description="Docker image for CASSS servers"

ADD . /opt/project
WORKDIR /opt/project

# Install base system required for build
RUN apk update && \
    apk add gcc g++ bash libzmq python3-dev && \
    apk add --update py3-pip &&\
    pip3 install --upgrade pip

# Install dependencies
RUN pip3 install -r requirements.txt

EXPOSE 5555

# CMD ["python","-u", "server.py"]
