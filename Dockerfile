FROM debian:latest
MAINTAINER Kostas Stamatiou <kostas.stamatiou@digitalglobe.com>

RUN apt-get update && \
    apt-get install -y \
      python \
      python-pip \
      git-core \
      build-essential \
      libsqlite3-dev \
      nano \
      zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install mapbox
RUN pip install mapbox

# install geojson
RUN pip install geojson

# install tippecanoe
RUN git clone https://github.com/mapbox/tippecanoe && \
    cd tippecanoe && \
    make && \
    make install && \
    cd .. && \
    rm -rf tippecanoe

ADD upload-to-mapbox.py /
ADD gbdx_task_interface.py /
