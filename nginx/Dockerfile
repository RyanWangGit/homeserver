FROM nginx:stable-alpine

RUN apk add --update --no-cache tini su-exec && \
    rm -rf /var/cache/apk/*

RUN addgroup -g ${PGID:-1000} nginx && \
    adduser -s /bin/false -G nginx -D -H -u ${PUID:-1000} nginx

COPY ./start_nginx.sh /start_nginx.sh

ENTRYPOINT ["tini", "--"]

CMD ["sh", "/start_nginx.sh"]
