FROM frolvlad/alpine-glibc

USER root

RUN apk add --update --no-cache ca-certificates wget glib libstdc++ python openssl tini && \
    wget https://www.dropbox.com/download?dl=packages/dropbox.py -O /usr/local/bin/dropbox-cli && \
    addgroup -g ${PGID:-1000} dropbox && \
    adduser -s /bin/false -G dropbox -D -h /dropbox -u ${PUID:-1000} dropbox && \
    mkdir -p /dropbox/.dropbox && \
    mkdir -p /dropbox/Dropbox && \
    cd /dropbox && \
    wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf - && \
    chmod +x /usr/local/bin/dropbox-cli && \
    chown dropbox:dropbox /usr/local/bin/dropbox-cli && \
    echo "Installed Dropbox version:" $(cat /dropbox/.dropbox-dist/VERSION)

USER dropbox

RUN ln -s /config/.dropbox /dropbox/.dropbox

WORKDIR /dropbox/Dropbox

EXPOSE 17500

VOLUME ["/dropbox/Dropbox"]

ENTRYPOINT ["tini", "--"]

CMD ["/dropbox/.dropbox-dist/dropboxd"]