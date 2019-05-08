FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends software-properties-common git maven wget ca-certificates

RUN apt-get install -y --no-install-recommends openjdk-8-jdk-headless openjdk-11-jdk-headless

RUN mkdir /minecraft
WORKDIR /minecraft

# first build spigot 1.14
RUN wget https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar
RUN java -jar BuildTools.jar nogui --rev 1.14

# create plugins folder
RUN mkdir -p plugins

# download pre-compiled plugins
# EssentialsX from https://ci.ender.zone/job/EssentialsX/
RUN wget https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/EssentialsX-2.16.1.154.jar \
    -O /minecraft/plugins/EssentialsX-2.16.1.154.jar

# then compile plugins that do not support 1.14 for pre-compiled version yet
# mcMMO
RUN mkdir /minecraft/plugin-sources
RUN cd /minecraft/plugin-sources && \
    git clone https://github.com/mcMMO-Dev/mcMMO.git && \
    cd mcMMO && \
    mvn clean install && \
    mv target/mcMMO.jar /minecraft/plugins

# WorldEdit
RUN cd /minecraft/plugin-sources && \
    git clone https://github.com/EngineHub/WorldEdit.git && \
    cd WorldEdit && \
    ./gradlew build -Dorg.gradle.java.home=/usr/lib/jvm/java-8-openjdk-amd64 && \
    cd worldedit-bukkit/build/libs && \
    mv worldedit-bukkit-7.0.0-SNAPSHOT-dist.jar /minecraft/plugins

# remove source folder
RUN rm -rf /minecraft/plugin-sources

COPY ./start_spigot.sh /start_spigot.sh

# remove jdk 8
RUN apt-get remove -y openjdk-8-jdk-headless
RUN apt-get autoremove -y

CMD ["sh", "/start_spigot.sh"]

EXPOSE 25565
VOLUME ["/config"]