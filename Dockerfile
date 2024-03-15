FROM python:3.6-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential\
    sqlite3

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000


CMD ["sqlite3", "todo.sqlite"] && [ "python3", "main.py" ]
