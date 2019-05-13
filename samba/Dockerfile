FROM alpine:edge

RUN apk upgrade --no-cache && \
    apk add --update --no-cache samba avahi tini && \
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

RUN for i in /etc/avahi/services/*; do mv $i ${i}.backup; done   
COPY smb.service /etc/avahi/services/smb.service

ENTRYPOINT ["tini", "--"]
CMD ["sh", "start_samba.sh"]

VOLUME ["/config", "/share"]

# 137, 138 for nmbd and 5353 for avahi
EXPOSE 135/tcp 137/udp 138/udp 5353/udp
