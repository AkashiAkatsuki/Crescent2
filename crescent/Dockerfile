FROM python:3.9.1
RUN apt-get update && apt-get install -y sudo git mecab libmecab-dev mecab-ipadic-utf8 busybox-static\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /opt/mecab-ipadic-neologd

WORKDIR /opt/mecab-ipadic-neologd
RUN bin/install-mecab-ipadic-neologd -n -y

WORKDIR /opt/crescent
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt \
    && pip install daphne

COPY . .
RUN touch logs/django.log


CMD bash -c "\
    python manage.py migrate &\
    daphne -b 0.0.0.0 -p 8080 project.asgi:fastapp &\
    daphne -b 0.0.0.0 -p 8081 project.asgi:application"
