FROM openjdk:11-jdk-slim AS builder

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends \
    software-properties-common \
    git \
    maven \
    wget \
    ca-certificates \
    openjdk-8-jdk-headless

RUN mkdir /minecraft
WORKDIR /minecraft

# first build spigot 1.14
RUN wget https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar
RUN java -jar BuildTools.jar nogui --rev 1.14 && \
    rm -rf BuildData && \
    rm -f BuildTools.jar

COPY ./build_plugins.sh /build_plugins.sh
RUN mkdir /plugins
RUN sh /build_plugins.sh

FROM openjdk:12-jdk-alpine3.9
COPY --from=builder /minecraft /minecraft
COPY --from=builder /plugins /plugins

WORKDIR /minecraft
COPY ./start_spigot.sh /start_spigot.sh

CMD ["sh", "/start_spigot.sh"]

EXPOSE 25565
VOLUME ["/config"]