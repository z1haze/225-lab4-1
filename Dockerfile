FROM python:3.9-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential\
    nfs-common\
    sqlite3

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000


CMD ["sqlite3", "todo.db"] && [ "python3", "main.py" ]
