FROM nginx:stable-alpine

RUN apk add --update --no-cache tini su-exec && \
    rm -rf /var/cache/apk/*

RUN addgroup -g 1000 abc && \
    adduser -s /bin/false -G abc -D -H -u 1000 abc

COPY ./start.sh /start.sh

ENTRYPOINT ["tini", "--"]

CMD ["sh", "/start.sh"]
