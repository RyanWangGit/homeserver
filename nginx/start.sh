#!/bin/sh

addgroup -g ${PGID:-1000} abc && \
adduser -s /bin/false -G abc -D -H -u ${PUID:-1000} abc

# create symlink if external config file exists
if [ -d "/config" ]; then
    if [ -f "/config/nginx.conf" ]; then 
        rm -f /etc/nginx/nginx.conf
        ln -s /config/nginx.conf /etc/nginx/nginx.conf
    else
        su-exec abc:abc cp /etc/nginx/nginx.conf /config/nginx.conf
    fi
    if [ -f "/config/php.ini" ]; then 
        rm -f /etc/php7/php.ini
        ln -s /config/php.ini /etc/php7/php.ini
    else
        su-exec abc:abc cp /etc/php7/php.ini /config/php.ini
    fi
    if [ -f "/config/php-fpm.conf" ]; then 
        rm -f /etc/php7/php-fpm.conf
        ln -s /config/php-fpm.conf /etc/php7/php-fpm.conf
    else
        su-exec abc:abc cp /etc/php7/php-fpm.conf /config/php-fpm.conf
    fi
fi

# start and daemonize php-fpm
su-exec abc:abc php-fpm7 -D

# start nginx
nginx -g "daemon off;"
