FROM openjdk:11-jre-slim
COPY ./start.sh /start.sh
COPY ./init.sh /init.sh

RUN mkdir /minecraft
WORKDIR /minecraft

# add tini
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl util-linux git wget ca-certificates && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    rm -rf /var/lib/apt/lists/*

# download paper server jar
RUN wget https://papermc.io/ci/job/Paper-1.14/lastSuccessfulBuild/artifact/paperclip.jar

# install the plugins
RUN mkdir /plugins
RUN ESSENTIALSX_JAR=`curl -s https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/ | grep -o "EssentialsX-[0-9.]*\.jar" | head -n1` && \
    wget "https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/${ESSENTIALSX_JAR}" \
    -O "/plugins/${ESSENTIALSX_JAR}"

# mcMMO
RUN wget https://popicraft.net/jenkins/job/mcMMO/lastSuccessfulBuild/artifact/mcMMO/target/mcMMO.jar \
    -O /plugins/mcMMO.jar

# WorldEdit
RUN wget https://media.forgecdn.net/files/2844/696/worldedit-bukkit-7.1.0-beta-1.jar \
    -O /plugins/worldedit-bukkit-7.1.0.jar

WORKDIR /minecraft

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/bin/sh", "/init.sh"]

EXPOSE 25565
VOLUME ["/config"]
