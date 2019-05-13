#!/bin/sh

# create correct symlink if external config is given
if [ -d /config ]; then
    if [ ! -f /config/smb.conf ]; then
        cp /etc/samba/smb.conf /config/smb.conf
    fi
    rm /etc/samba/smb.conf
    ln -s /config/smb.conf /etc/samba/smb.conf
fi

mkdir -p /usr/local/samba
mkdir -p /usr/local/samba/var/
ln -s /usr/local/samba/var /logs

# start samba daemon and avahi daemon
smbd
avahi-daemon 2> /logs/log.avahid
tail -f /logs/log.smbd /logs/log.avahid