migrate:
	sudo docker compose -f ../docker-compose.production.yml exec food-backend python manage.py migrate
	sudo docker compose -f ../docker-compose.production.yml exec food-backend python manage.py collectstatic --noinput
add_db:
	sudo docker compose -f ../docker-compose.production.yml exec food-backend python manage.py add_db
	sudo docker compose -f ../docker-compose.production.yml exec food-backend python manage.py loaddata ./data/tags.json
su:
	sudo docker compose -f ../docker-compose.production.yml exec food-backend python manage.py createsuperuser
