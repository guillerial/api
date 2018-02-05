include .env
export $(shell sed 's/=.*//' .env)
PYTHON=$(PWD)/.venv/bin/python

createsuperuser: .env .venv
	cd api && $(PYTHON) ./manage.py createsuperuser

runserver: .env .venv migrate
	cd api && $(PYTHON) ./manage.py runserver 0.0.0.0:8000

migrate: .env .venv
	cd api && $(PYTHON) ./manage.py makemigrations
	cd api && $(PYTHON) ./manage.py migrate

inspectdb: .env .venv migrate
	cd api && $(PYTHON) ./manage.py inspectdb

.venv: .venv/bin/activate

.venv/bin/activate: requirements.txt
	test -d .venv || python3 -m venv .venv
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

.env:
	cp .env.sample .env


