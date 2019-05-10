#!/bin/sh

# download pre-compiled plugins
# EssentialsX from https://ci.ender.zone/job/EssentialsX/
wget https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/EssentialsX-2.16.1.154.jar \
    -O /plugins/EssentialsX-2.16.1.154.jar

# then compile plugins that do not support 1.14 for pre-compiled version yet
# mcMMO
mkdir /tmp/plugin-sources
cd /tmp/plugin-sources
git clone https://github.com/mcMMO-Dev/mcMMO.git
cd mcMMO
mvn clean install 
mv target/mcMMO.jar /plugins/

# WorldEdit
cd /tmp/plugin-sources
git clone https://github.com/EngineHub/WorldEdit.git
cd WorldEdit
./gradlew build -Dorg.gradle.java.home=/usr/lib/jvm/java-8-openjdk-amd64 
cd worldedit-bukkit/build/libs
mv worldedit-bukkit-7.0.0-SNAPSHOT-dist.jar /plugins/

# remove source folder
rm -rf /tmp/plugin-sources