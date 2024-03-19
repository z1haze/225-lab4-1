FROM python:3.9-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential\
    nfs-common\
    nfs-utils

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["sudo mount -t nfs://10.48.228.21/roseaw /mnt/srv/samba/roseaw -o guest,iocharset=utf8"], && ["python3", "main.py" ]
