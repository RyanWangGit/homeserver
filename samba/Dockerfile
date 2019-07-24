FROM alpine:edge

RUN apk upgrade --no-cache && \
    apk add --update --no-cache samba avahi tini su-exec && \
    rm -rf /var/cache/apk/*

COPY ./start_samba.sh /start_samba.sh

RUN sed -i "s/workgroup = MYGROUP/workgroup = WORKGROUP/g" /etc/samba/smb.conf && \
    sed -i "s/server string = Samba Server/server string = Homeserver Samba/g" /etc/samba/smb.conf && \
    sed -i 's/#enable-dbus=yes/enable-dbus=no/g' /etc/avahi/avahi-daemon.conf

RUN echo "[share]" >> /etc/samba/smb.conf && \
    echo "   path = /share" >> /etc/samba/smb.conf && \
    echo "   public = yes" >> /etc/samba/smb.conf && \
    echo "   read only = yes" >> /etc/samba/smb.conf && \
    echo "   only guest = yes" >> /etc/samba/smb.conf

RUN rm /etc/avahi/services/*   
COPY smb.service /etc/avahi/services/smb.service

ENTRYPOINT ["tini", "--"]
CMD ["sh", "start.sh"]

VOLUME ["/config", "/share"]

# 445 for smbd and 5353 for avahi
EXPOSE 445/tcp 5353/udp
