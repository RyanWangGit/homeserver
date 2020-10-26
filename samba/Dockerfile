FROM lsiobase/alpine:3.12

RUN apk add --no-cache samba

COPY /root /

VOLUME ["/config", "/share"]

# 445 for smbd
EXPOSE 445/tcp
