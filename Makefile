clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
	rm -rf migrations
	rm sme_financing/main/*.db

upgrade-db:
	python manage.py db migrate
	python manage.py db upgrade

init-db:
	python manage.py db init

all-db: init-db upgrade-db

tests:
	python manage.py test

run:
	python manage.py run

sort-import:
	poetry isort -rc .

format:
	poetry run black .

