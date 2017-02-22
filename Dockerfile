FROM debian:latest
MAINTAINER Kostas Stamatiou <kostas.stamatiou@digitalglobe.com>

RUN apt-get update && \
    apt-get install -y python python-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install mapbox
RUN pip install mapbox

ADD upload-to-mapbox.py /
ADD gbdx_task_interface.py /
