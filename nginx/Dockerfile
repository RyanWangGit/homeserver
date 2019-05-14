FROM nginx:stable-alpine

RUN apk --update --no-cache tini && \
    rm -rf /var/cache/apk/*

COPY ./start_nginx.sh /start_nginx.sh

ENTRYPOINT ["tini", "--"]

CMD ["sh", "/start_nginx.sh"]
