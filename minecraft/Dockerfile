FROM alpine:3.12 AS builder

RUN mkdir /minecraft
WORKDIR /minecraft

RUN apk add --no-cache \
    curl \
    git \
    wget \
    ca-certificates \
    pcre-tools

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
RUN VIABACKWARDS_JAR=`curl -s https://ci.viaversion.com/view/ViaBackwards/job/ViaBackwards/lastSuccessfulBuild/artifact/all/target/ | pcregrep -o "ViaBackwards-[0-9.]*(-\w*)?.jar" | head -n1` && \
    wget "https://ci.viaversion.com/view/ViaBackwards/job/ViaBackwards/lastSuccessfulBuild/artifact/all/target/${VIABACKWARDS_JAR}" \
    -O "/plugins/${VIABACKWARDS_JAR}"
    
# Dynmap
RUN DYNMAP_JAR=`curl -s https://dynmap.us/builds/dynmap/ | pcregrep -o1 "\"(Dynmap-[\d.]*-SNAPSHOT-spigot\.jar)\"" | sort -V -r | head -n1` && \
    wget "https://dynmap.us/builds/dynmap/${DYNMAP_JAR}" \
    -O "/plugins/${DYNMAP_JAR}"


FROM lsiobase/alpine:3.12

COPY --from=builder /minecraft /minecraft
COPY --from=builder /plugins /plugins

WORKDIR /minecraft

# install python3
RUN apk add --no-cache python3 py3-pip 

# install uvloop
RUN apk add --no-cache make gcc g++ python3-dev \
    && pip3 install -U wheel pip \
    && pip3 install uvloop coloredlogs \
    && apk del make gcc g++ python3-dev 

# install openjdk
RUN apk add --no-cache openjdk15-jre-headless --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing

COPY root/ /

EXPOSE 25565
VOLUME /config