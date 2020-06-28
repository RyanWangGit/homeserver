#!/bin/bash

# handles EULA
if [ ! -z $EULA ]; then 
    echo "eula=$EULA" > /minecraft/eula.txt
fi

# copy the compiled plugins to config folder
mkdir -p /config/plugins

# remove older plugins
rm -f /config/plugins/EssentialsX-*.jar
rm -f /config/plugins/mcMMO*.jar
rm -f /config/plugins/worldedit-bukkit*.jar
rm -f /config/plugins/viaversion*.jar
rm -f /config/plugins/viabackwards*.jar

# copy compiled plugins
cp /plugins/*.jar /config/plugins/

# create world folder if not present
mkdir -p /config/world

# symlinks the config files that cannot be specified from command line to spigot
rm -f /minecraft/ops.json
rm -f /minecraft/permissions.yml
rm -f /minecraft/whitelist.json
rm -f /minecraft/wepif.yml
ln -s /config/ops.json /minecraft/ops.json
ln -s /config/permissions.yml /minecraft/permissions.yml
ln -s /config/whitelist.json /minecraft/whitelist.json
ln -s /config/wepif.yml /minecraft/wepif.yml

# start the paper server using user `minecraft`
LOCAL_IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.*' | grep -v '172.*' | grep -m1 '')
python3 mcmanager.py $LOCAL_IP 25565 127.0.0.1 25564 "/minecraft/paperclip.jar nogui --noconsole -c /config/server.properties -b /config/bukkit.yml -S /config/spigot.yml --paper /config/paper.yml -C /config/commands.yml -W /config/world -P /config/plugins" "-Xmx1024M -Xms512M -XX:MinHeapFreeRatio=20 -XX:MaxHeapFreeRatio=50"
