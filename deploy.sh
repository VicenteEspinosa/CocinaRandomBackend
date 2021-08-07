#!/bin/sh 
sudo git pull origin main
source .env
poetry install
poetry run python cocina/manage.py makemigrations
poetry run python cocina/manage.py migrate
poetry run python cocina/manage.py collectstatic
