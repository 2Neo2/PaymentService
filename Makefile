db-up:
	docker compose -f docker/docker-compose.yml up

db-reset:
	docker compose -f docker/docker-compose.yml down -v

django-server:
	cd src && python3 manage.py runserver

migrations:
	cd src && python3 manage.py makemigrations

migrate:
	cd src && python3 manage.py migrate

shell:
	cd src && python3 manage.py shell

createsuperuser:
	cd src && python3 manage.py createsuperuser