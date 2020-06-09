clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
	rm -rf migrations
	rm sme_financing/main/*.db

insert:
	python manage.py insert

upgrade-db:
	python manage.py db migrate
	python manage.py db upgrade

init-db:
	python manage.py db init

all-db: init-db upgrade-db insert

tests:
	poetry run pytest --disable-warnings

test-all:
	pytest --disable-warnings -v

run:
	python manage.py run

lint:
	poetry run flake8 . --count --show-source --statistics

sort-import:
	poetry run isort -rc .

fmt:
	poetry run black .
