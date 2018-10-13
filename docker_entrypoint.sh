#!/bin/bash

python excelplay-auth/excelplay_auth/manage.py makemigrations && \
	python excelplay-auth/excelplay_auth/manage.py migrate
cd excelplay-auth/excelplay_auth
gunicorn excelplay_auth.wsgi --bind 0.0.0.0:8000
