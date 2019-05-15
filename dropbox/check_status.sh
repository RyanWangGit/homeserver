#!/bin/sh
STORED="";
while true
do
    if [ -f '/dropbox/.dropbox-dist/VERSION' ]; then
        CUR="$(dropbox-cli status)";
        if [ "$STORED" != "$CUR" ]; then
            STORED="$CUR"
            echo "${STORED}"
        fi
    fi
    sleep 60
done