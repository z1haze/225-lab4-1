FROM python:3.6-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "main.py" ]
