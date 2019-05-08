#!/bin/bash

# handles EULA
if [ ! -z $EULA ]; then 
    echo "eula=$EULA" > /minecraft/eula.txt
fi

# create world folder if not present
mkdir -p /config/world

# start the spigot server
java -Xmx2048M -Xms2048M -jar /minecraft/spigot-1.14.jar nogui \
    -c /config/server.properties \
    -b /config/bukkit.yml \
    -S /config/spigot.yml \
    -C /config/commands.yml \
    -W /config/world
