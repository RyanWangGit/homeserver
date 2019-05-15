FROM frolvlad/alpine-glibc

USER root

RUN apk add --update --no-cache ca-certificates wget glib libstdc++ python3 openssl tini && \
    wget https://www.dropbox.com/download?dl=packages/dropbox.py -O /usr/local/bin/dropbox-cli && \
    addgroup -g ${PGID:-1000} dropbox && \
    adduser -s /bin/false -G dropbox -D -h /dropbox -u ${PUID:-1000} dropbox && \
    mkdir -p /dropbox/.dropbox && \
    mkdir -p /dropbox/Dropbox && \
    cd /dropbox && \
    wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf - && \
    chmod +x /usr/local/bin/dropbox-cli && \
    chown dropbox:dropbox /usr/local/bin/dropbox-cli && \
    chown -R dropbox:dropbox /dropbox && \
    echo "Installed Dropbox version:" $(cat /dropbox/.dropbox-dist/VERSION)

USER dropbox

WORKDIR /dropbox/Dropbox

ADD check_status.sh /dropbox/check_status.sh
ADD start_dropbox.sh /dropbox/start_dropbox.sh
RUN chmod +x /dropbox/check_status.sh && \
    chmod +x /dropbox/start_dropbox.sh

EXPOSE 17500

VOLUME ["/dropbox/Dropbox"]

ENTRYPOINT ["tini", "--"]

CMD ["/dropbox/start_dropbox.sh"]