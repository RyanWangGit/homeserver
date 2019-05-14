FROM nginx:stable-alpine

RUN apk add --update --no-cache tini su-exec && \
    rm -rf /var/cache/apk/*

RUN addgroup -g ${PGID:-1000} normal && \
    adduser -s /bin/false -G normal -D -H -u ${PUID:-1000} normal

COPY ./start_nginx.sh /start_nginx.sh

ENTRYPOINT ["tini", "--"]

CMD ["sh", "/start_nginx.sh"]
