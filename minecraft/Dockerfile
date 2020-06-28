FROM openjdk:14-slim
COPY ./start.sh /start.sh
COPY ./init.sh /init.sh

RUN mkdir /minecraft
WORKDIR /minecraft

# add tini
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl util-linux git wget ca-certificates python3 python3-pip net-tools pcregrep && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    rm -rf /var/lib/apt/lists/*

# add uvloop and coloredlogs
RUN pip3 install -U setuptools pip
RUN pip3 install --no-cache-dir uvloop coloredlogs

# download paper server jar
RUN PAPERCLIP_JAR=`curl -s https://papermc.io/ci/job/Paper-1.16/lastSuccessfulBuild/artifact/ | grep -o "paperclip-[0-9]*\.jar" | head -n1` && \
    wget "https://papermc.io/ci/job/Paper-1.16/lastSuccessfulBuild/artifact/${PAPERCLIP_JAR}" \
    -O paperclip.jar

# download manager python wrapper
RUN wget https://gist.githubusercontent.com/yxwangcs/b82abf7424d02b384e4e5ee5985552b1/raw/mcmanager.py

# install the plugins
RUN mkdir /plugins
RUN ESSENTIALSX_JAR=`curl -s https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/ | grep -o "EssentialsX-[0-9.]*\.jar" | head -n1` && \
    wget "https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/Essentials/target/${ESSENTIALSX_JAR}" \
    -O "/plugins/${ESSENTIALSX_JAR}"

# mcMMO
RUN wget https://papermc.io/ci/view/all/job/mcMMO/lastSuccessfulBuild/artifact/target/mcMMO.jar \
    -O /plugins/mcMMO.jar

# WorldEdit
RUN WORLDEDIT_JAR=`curl -s https://builds.enginehub.org/job/worldedit/last-successful\?branch\=master | grep -o "worldedit-bukkit-[0-9.]*-\w*-\w*\.jar" | head -n1` && \
    BUILD_NUMBER=`curl -s https://builds.enginehub.org/job/worldedit/last-successful\?branch\=master | pcregrep -o1 "\"build_id\":([0-9]*)"` && \
    BUILD_TYPE=`curl -s https://builds.enginehub.org/job/worldedit/last-successful\?branch\=master | pcregrep -o1 "\"buildType\":\"([\w\d]*)\""` && \
    wget "https://ci.enginehub.org/repository/download/${BUILD_TYPE}/${BUILD_NUMBER}:id/${WORLDEDIT_JAR}?branch=master&guest=1" \
    -O "/plugins/${WORLDEDIT_JAR}"
    
# viaversion
RUN VIAVERSION_JAR=`curl -s https://ci.viaversion.com/job/ViaVersion/lastSuccessfulBuild/artifact/jar/target/ | grep -o "ViaVersion-[0-9.]*-\w*.jar" | head -n1` && \
    wget "https://ci.viaversion.com/job/ViaVersion/lastSuccessfulBuild/artifact/jar/target/${VIAVERSION_JAR}" \
    -O "/plugins/${VIAVERSION_JAR}"
    
# viabackwards
RUN VIABACKWARDS_JAR=`curl -s https://ci.viaversion.com/view/ViaBackwards/job/ViaBackwards/lastSuccessfulBuild/artifact/all/target/ | grep -o "ViaBackwards-[0-9.]*-\w*.jar" | head -n1` && \
    wget "https://ci.viaversion.com/view/ViaBackwards/job/ViaBackwards/lastSuccessfulBuild/artifact/all/target/${VIABACKWARDS_JAR}" \
    -O "/plugins/${VIABACKWARDS_JAR}"
    
# Dynmap
RUN DYNMAP_JAR=`curl -s https://dynmap.us/builds/dynmap/ | pcregrep -o1 "\"(Dynmap-[\d.]*-SNAPSHOT-spigot\.jar)\"" | sort -V -r | head -n1` && \
    wget "https://dynmap.us/builds/dynmap/${DYNMAP_JAR}" \
    -O "/plugins/${DYNMAP_JAR}"

WORKDIR /minecraft

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/bin/sh", "/init.sh"]

EXPOSE 25565
VOLUME ["/config"]
