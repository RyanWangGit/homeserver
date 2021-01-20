FROM ghcr.io/linuxserver/baseimage-alpine:3.13

RUN apk add --no-cache samba

COPY /root /

VOLUME ["/config", "/share"]

# 445 for smbd
EXPOSE 445/tcp
