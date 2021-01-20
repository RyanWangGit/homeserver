FROM ghcr.io/linuxserver/baseimage-alpine:3.13

RUN mkdir /minecraft
WORKDIR /minecraft

# install python3
RUN apk add --no-cache python3 py3-pip 
RUN pip3 install requests tqdm

# copy the jar updater script
COPY ./jar_updater.py /jar_updater.py

# install uvloop
RUN apk add --no-cache make gcc g++ python3-dev \
    && pip3 install -U wheel pip \
    && pip3 install uvloop coloredlogs \
    && apk del make gcc g++ python3-dev 

# install openjdk
RUN apk add --no-cache openjdk15 maven --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing
RUN apk add git

COPY root/ /

EXPOSE 25565
VOLUME /config