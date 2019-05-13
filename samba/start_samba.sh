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
ln -s /logs /usr/local/samba/var/

# start samba daemon and netbios daemon
smbd && nmbd
tail -F /logs/log.smbd