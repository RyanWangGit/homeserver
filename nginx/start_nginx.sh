#!/bin/sh

# create symlink if external config file exists
if [ -d "/config" ]; then
    if [ -f "/config/nginx.conf" ]; then 
        rm -f /etc/nginx/nginx.conf
        ln -s /config/nginx.conf /etc/nginx/nginx.conf
    else
        su-exec abc:abc cp /etc/nginx/nginx.conf /config/nginx.conf
    fi
fi

# start nginx
nginx -g "daemon off;"
