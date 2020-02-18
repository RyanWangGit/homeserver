FROM nginx:stable-alpine

RUN apk add --update --no-cache tini su-exec && \
    rm -rf /var/cache/apk/*

COPY ./start.sh /start.sh

ENTRYPOINT ["tini", "--"]

CMD ["sh", "/start.sh"]
