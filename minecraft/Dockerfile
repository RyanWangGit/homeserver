FROM openjdk:11-jdk-slim AS builder

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    git \
    maven \
    wget \
    ca-certificates

RUN mkdir /minecraft
WORKDIR /minecraft

# first build spigot 1.14
RUN wget https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar
RUN java -jar BuildTools.jar nogui --rev 1.14.2 && \
    rm -rf BuildData && \
    rm -f BuildTools.jar

# install the plugins
RUN mkdir /plugins
RUN ESSENTIALSX_JAR=`curl -s https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/ | grep -o "EssentialsX-[0-9.]*\.jar" | head -n1` && \
    wget "https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/${ESSENTIALSX_JAR}" \
    -O "/plugins/${ESSENTIALSX_JAR}"

# then compile plugins that do not support 1.14 for pre-compiled version yet
# mcMMO
RUN mkdir /tmp/plugin-sources && cd /tmp/plugin-sources && \
    git clone https://github.com/mcMMO-Dev/mcMMO.git && \
    cd mcMMO && \
    mvn clean install && \
    mv target/mcMMO.jar /plugins/

# WorldEdit
RUN wget https://media.forgecdn.net/files/2711/407/worldedit-bukkit-7.0.0-rc-2.jar \
    -O /plugins/worldedit-bukkit-7.0.0-rc-2.jar

# create new slim image to store the compiled files
FROM openjdk:11-jre-slim
COPY --from=builder /minecraft /minecraft
COPY --from=builder /plugins /plugins
COPY ./start_spigot.sh /start_spigot.sh

# create a normal user
RUN groupadd -f -g ${PGID:-1000} minecraft && \
    useradd -g ${PGID:-1000} -M -u ${PUID:-1000} -s /bin/false minecraft

# change the permissions of the files we will use
RUN mkdir -p /config && \
    chown minecraft:minecraft /config && \
    chown -R minecraft:minecraft /minecraft && \
    chown -R minecraft:minecraft /plugins && \
    chown minecraft:minecraft /start_spigot.sh

# add tini
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl setpriv && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /minecraft

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["setpriv", "--reuid=minecraft", "--regid=minecraft", "--clear-groups", "bash", "/start_spigot.sh"]

EXPOSE 25565
VOLUME ["/config"]