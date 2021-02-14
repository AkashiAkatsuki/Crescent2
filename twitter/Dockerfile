FROM python:3.9.1

RUN apt-get update && apt-get install -y busybox-static\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/twitter
COPY twitter/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY twitter/crontab /var/spool/cron/crontabs/root

CMD bash -c "\
  busybox crond -f -L /dev/stderr &\
  python main.py start"
