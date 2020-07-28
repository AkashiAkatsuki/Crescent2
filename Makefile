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
