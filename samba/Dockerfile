FROM alpine:edge

RUN apk add --update samba tini && \
    rm -rf /var/cache/apk/*

COPY ./start_samba.sh /start_samba.sh

RUN sed -i "s/workgroup = MYGROUP/workgroup = WORKGROUP/g" /etc/samba/smb.conf && \
    sed -i "s/server string = Samba Server/server string = Homeserver Samba/g" /etc/samba/smb.conf

RUN echo "[share]" >> /etc/samba/smb.conf && \
    echo "   path = /share" >> /etc/samba/smb.conf && \
    echo "   public = yes" >> /etc/samba/smb.conf && \
    echo "   read only = yes" >> /etc/samba/smb.conf && \
    echo "   only guest = yes" >> /etc/samba/smb.conf

ENTRYPOINT ["tini", "--", "sh", "start_samba.sh"]

VOLUME ["/config", "/share"]

# 137, 138 for nmbd and 139, 445 for smbd
EXPOSE 135/tcp 137/udp 138/udp 139/tcp 445/tcp
