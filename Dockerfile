FROM ubuntu:24.04 AS base

RUN set -e

ENV DEBIAN_FRONTEND=noninteractive
ENV GIT_SSL_NO_VERIFY=1

# Install packages
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends\
        g++\
        gcc\
        make\
        curl\
        time\
        libgmp-dev\
        ca-certificates\
        ppl-dev\
        just

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY . /opt/artifact
WORKDIR /opt/artifact/

RUN uv sync
RUN uv pip install polars

WORKDIR /opt/artifact
