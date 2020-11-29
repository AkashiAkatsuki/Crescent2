FROM python:3.8
RUN apt-get update && apt-get install -y sudo git mecab libmecab-dev mecab-ipadic-utf8 busybox-static\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /opt/mecab-ipadic-neologd

WORKDIR /opt/mecab-ipadic-neologd
RUN bin/install-mecab-ipadic-neologd -n -y

WORKDIR /opt/crescent
COPY crescent/requirements.txt requirements.txt
RUN pip install -r requirements.txt \
    && pip install daphne

COPY crescent/crontab /var/spool/cron/crontabs/root
