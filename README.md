# Homeserver - Docker
This is a docker setup for a fully-dockerized homeserver, inspired by [this reddit post](https://www.reddit.com/r/docker/comments/7ro9lv/why_shouldnt_i_dockerize_everything_on_my_server/). This is mainly a docker setup for my own homeserver use case, but thanks to the modularity of containers, it can easily be adapted to yours as well.

## Overview
The philoshophy of this project is that it should be easy to backup / migrate. To do that, we start by a barebone OS (debian/redhat or whatever that supports docker), and then run all applications in containers with a central config folder. This gives us a very clean design and makes it super easy to migrate or update your server. See [docker-compose.yml](https://github.com/yxwangcs/homeserver/blob/master/docker-compose.yml) for the detailed settings.

## Setup Notes
I'm using [mergerfs](https://github.com/trapexit/mergerfs) to group together a bunch of external usb drives with different sizes (mounted at `/mnt/usb`). So the data volumes for the many containers are mapped to `/mnt/usb/media`. For easy management, all configs for the applications are stored in `/config/<application name>` in the host machine and mapped to `/config` folder inside containers, and I use rclone (whose config is stored at `/rclone`) to back them up everyday to my google drive. There is a non-priviledged user `abc` with PUID:PGIG=1000:1000 for you to use, I try to use this user as much as possible for security reasons, but most of the time you can pass in `$PUID$` and `$PGID$` environment variables to change the corresponding value.

## Containers
This project contains many `Dockerfile`s in folders to build each individual application that I personally run on my homeserver. Refer to [docker-compose.yml](https://github.com/yxwangcs/homeserver/blob/master/docker-compose.yml) for details.

## License
[MIT](https://github.com/yxwangcs/homeserver/blob/master/LICENSE).
