build:
	docker-compose build

prod-up-d:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d

prod-up:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up

dev-up-d:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d

dev-up:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml up

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

shell-nginx:
	docker exec -ti nz01 bash

shell-web:
	docker exec -ti dz01 bash

shell-db:
	docker exec -ti pz01 bash

log-nginx:
	docker-compose logs nginx  

log-web:
	docker-compose logs web  

log-db:
	docker-compose logs db

collectstatic:
	docker exec dz01 /bin/sh -c "python manage.py collectstatic --noinput"