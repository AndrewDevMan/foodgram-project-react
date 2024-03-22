db-up:
	sudo docker compose -f ./docker-compose_db.yml up -d
db-down:
	sudo docker compose -f ./docker-compose_db.yml down
up:
	sudo docker compose up -d
down:
	sudo docker compose down
migrate:
	sudo docker compose exec food-backend python manage.py migrate
	sudo docker compose exec food-backend python manage.py collectstatic -y
	sudo docker compose exec food-backend python manage.py add_db
	sudo docker compose exec food-backend python manage.py loaddata ./data/tags.json
su:
	sudo docker compose exec food-backend python manage.py createsuperuser
