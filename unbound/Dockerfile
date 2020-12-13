FROM alpine:3.12 AS builder

RUN apk add --no-cache \
    build-base \
    clang \
    curl \
    expat-dev \
    expat-static \
    linux-headers \
    libevent-dev \
    libevent-static \
    libressl-dev \
    perl

WORKDIR /tmp/unbound

ARG UNBOUND_SOURCE=https://www.nlnetlabs.nl/downloads/unbound/unbound-
ARG UNBOUND_VERSION=1.13.0
ARG UNBOUND_SHA256=a954043a95b0326ca4037e50dace1f3a207a0a19e9a4a22f4c6718fc623db2a1

RUN curl -fsSL --retry 3 "${UNBOUND_SOURCE}${UNBOUND_VERSION}.tar.gz" -o unbound.tar.gz \
    && echo "${UNBOUND_SHA256}  unbound.tar.gz" | sha256sum -c - \
    && tar xzf unbound.tar.gz --strip 1 \
    && CC=clang ./configure --with-pthreads --with-libevent --enable-event-api --prefix=/opt/unbound --with-run-dir=/var/run/unbound --with-username=abc --with-chroot-dir= --enable-fully-static --disable-shared \
    && make -j 4 install

RUN rm -rf /tmp/* /opt/*/include /opt/*/man /opt/*/share \
    && strip /opt/unbound/sbin/unbound


FROM ghcr.io/linuxserver/baseimage-alpine:3.12

COPY --from=builder /opt /opt

RUN apk --no-cache add dns-root-hints

COPY root/ /

EXPOSE 5353
VOLUME /config