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
rm -f /config/plugins/worldedit-bukkit-*.jar

# move compiled plugins
mv /plugins/*.jar /config/plugins/

# create world folder if not present
mkdir -p /config/world

# symlinks the config files that cannot be specified from command line to spigot
ln -s /config/ops.json /minecraft/ops.json
ln -s /config/permissions.yml /minecraft/permissions.yml
ln -s /config/whitelist.json /minecraft/whitelist.json
ln -s /config/wepif.yml /minecraft/wepif.yml

# start the spigot server using user `minecraft`
java -Xmx2048M -Xms512M -jar /minecraft/spigot-1.14.2.jar nogui \
    --noconsole \
    -c /config/server.properties \
    -b /config/bukkit.yml \
    -S /config/spigot.yml \
    -C /config/commands.yml \
    -W /config/world \
    -P /config/plugins
