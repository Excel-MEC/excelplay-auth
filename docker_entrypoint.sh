#!/bin/bash

python excelplay-auth/excelplay_auth/manage.py makemigrations && \
	python excelplay-auth/excelplay_auth/manage.py migrate
gunicorn excelplay-auth/excelplay_auth/excelplay_auth.wsgi --bind 0.0.0.0:8000
