FROM    debian

COPY    . /root/

ARG     DEBIAN_FRONTEND=noninteractive

RUN     \
    sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y dialog apt-utils && \
    apt-get upgrade -y && \
    apt-get clean

RUN     \
    apt-get install -y python3 python3-pip openssh-server && \
    apt-get clean && \
    python3 -m pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

EXPOSE 22

CMD [ "/bin/bash", "/root/docker.sh"]
