#!/bin/bash

python excelplay-auth/excelplay_auth/manage.py makemigrations && \
	python excelplay-auth/excelplay_auth/manage.py migrate
python excelplay-auth/excelplay_auth/manage.py runserver 0.0.0.0:8000
