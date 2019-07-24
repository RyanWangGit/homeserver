#!/bin/sh

# add a non-priviledged user
groupadd -f -g ${PGID:-1000} abc
useradd -g ${PGID:-1000} -M -u ${PUID:-1000} -s /bin/false abc

# change the permissions of the files we will use
mkdir -p /config
chown abc:abc /config
chown -R abc:abc /minecraft
chown -R abc:abc /plugins
chown abc:abc /start.sh

setpriv --reuid=abc --regid=abc --clear-groups /start.sh