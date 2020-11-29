include .env

up:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose build --no-cache
migrate:
	docker-compose exec crescent python manage.py migrate
bash:
	docker-compose exec crescent /bin/bash
shell:
	docker-compose exec crescent python manage.py shell
test:
	docker-compose exec crescent python manage.py test ${app}
pip-install:
	docker-compose exec crescent pip install -r requirements.txt
twitter:
	docker-compose exec crescent python manage.py twitter_stream
psql:
	psql -h localhost -p $(DB_PORT_LOCAL) -U $(POSTGRES_USER) $(POSTGRES_DB)
dump:
	pg_dump -h localhost -p $(DB_PORT_LOCAL) -U $(POSTGRES_USER) $(POSTGRES_DB) > ${file}
restore:
	psql -h localhost -p $(DB_PORT_LOCAL) -U $(POSTGRES_USER) $(POSTGRES_DB) < ${file}
