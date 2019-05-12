FROM alpine:edge

RUN apk add --update samba tini && \
    rm -rf /var/cache/apk/*


COPY ./start_samba.sh /start_samba.sh

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["sh", "start_samba.sh"]