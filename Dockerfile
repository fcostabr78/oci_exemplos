FROM ubuntu:16.04
LABEL maintainer="fernando.d.costa@oracle.com"
RUN apt-get update
RUN apt-get install -y python3