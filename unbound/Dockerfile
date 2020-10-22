FROM alpine:3.12 AS builder

RUN apk add --no-cache \
    build-base \
    clang \
    curl \
    expat-dev \
    expat-static \
    linux-headers \
    openssl-dev \
    openssl-libs-static \
    perl

WORKDIR /tmp/unbound

ARG UNBOUND_SOURCE=https://www.nlnetlabs.nl/downloads/unbound/unbound-
ARG UNBOUND_VERSION=1.12.0
ARG UNBOUND_SHA1=68009078d5f5025c95a8c9fe20b9e84335d53e2d

RUN curl -fsSL --retry 3 "${UNBOUND_SOURCE}${UNBOUND_VERSION}.tar.gz" -o unbound.tar.gz \
    && echo "${UNBOUND_SHA1}  unbound.tar.gz" | sha1sum -c - \
    && tar xzf unbound.tar.gz --strip 1 \
    && CC=clang ./configure --with-pthreads --prefix=/opt/unbound --with-run-dir=/var/run/unbound --with-username=abc --with-chroot-dir= --enable-fully-static --disable-shared \
    && make -j 4 install

RUN rm -rf /tmp/* /opt/*/include /opt/*/man /opt/*/share \
    && strip /opt/unbound/sbin/unbound


FROM lsiobase/alpine:3.12

COPY --from=builder --chown=abc:abc /opt /opt

RUN apk --no-cache add dns-root-hints

COPY root/ /

EXPOSE 5353
VOLUME /config