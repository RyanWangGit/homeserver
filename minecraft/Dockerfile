FROM openjdk:11-jdk-slim AS builder

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends \
    software-properties-common \
    git \
    maven \
    wget \
    ca-certificates

RUN mkdir /minecraft
WORKDIR /minecraft

# first build spigot 1.14
RUN wget https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar
RUN java -jar BuildTools.jar nogui --rev 1.14 && \
    rm -rf BuildData && \
    rm -f BuildTools.jar

# install the plugins
RUN mkdir /plugins
RUN wget https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/EssentialsX-2.16.1.155.jar \
    -O /plugins/EssentialsX-2.16.1.154.jar

# then compile plugins that do not support 1.14 for pre-compiled version yet
# mcMMO
RUN mkdir /tmp/plugin-sources && cd /tmp/plugin-sources && \
    git clone https://github.com/mcMMO-Dev/mcMMO.git && \
    cd mcMMO && \
    mvn clean install && \
    mv target/mcMMO.jar /plugins/

# WorldEdit
RUN wget http://builds.enginehub.org/job/worldedit/11630/download/worldedit-bukkit-7.0.0-SNAPSHOT-dist.jar \
    -O /plugins/worldedit-bukkit-7.0.0-SNAPSHOT-dist.jar

# create new slim image to store the compiled files
FROM openjdk:11-jre-slim
COPY --from=builder /minecraft /minecraft
COPY --from=builder /plugins /plugins

WORKDIR /minecraft
COPY ./start_spigot.sh /start_spigot.sh

CMD ["sh", "/start_spigot.sh"]

EXPOSE 25565
VOLUME ["/config"]