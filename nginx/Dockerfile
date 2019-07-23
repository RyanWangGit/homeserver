FROM nginx:stable-alpine

RUN apk add --update --no-cache tini su-exec && \
    rm -rf /var/cache/apk/*

RUN addgroup -g 1000 normal && \
    adduser -s /bin/false -G normal -D -H -u 1000 normal

COPY ./start_nginx.sh /start_nginx.sh

ENTRYPOINT ["tini", "--"]

CMD ["sh", "/start_nginx.sh"]
