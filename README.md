# Homeserver - Docker
This is a docker setup for a fully-dockerized homeserver, inspired by [this reddit post](https://www.reddit.com/r/docker/comments/7ro9lv/why_shouldnt_i_dockerize_everything_on_my_server/). This is mainly a docker setup for my own homeserver use case, but thanks to the modularity of containers, it can easily be adapted to yours as well.

## Overview
The philoshophy of this project is that you should have much control over your own server. That is, we start by a barebone OS (debian/redhat or whatever that supports docker), and we run all applications in containers with a central config folder that is easy to back up. This gives us a very clean design and makes it super easy to migrate or update your server.

## Setup Notes


## Containers
This project contains many `Dockerfile`s in folders to build each individual application that I personally run on my homeserver.

### Plex

### Transmission

### Samba

### Minecraft
[Spigot](https://www.spigotmc.org/) 1.14 minecraft server with [EssentialsX](https://github.com/EssentialsX/Essentials), [mcMMO](https://github.com/mcMMO-Dev/mcMMO) and [WorldEdit](https://github.com/EngineHub/WorldEdit) plugins.

## License
[MIT](https://github.com/RyanWangGit/homeserver/blob/master/LICENSE).
