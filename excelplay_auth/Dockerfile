FROM python:3.6
 ENV PYTHONUNBUFFERED 1
 RUN mkdir -p /excelplay/excelplay_auth
 WORKDIR /excelplay/excelplay_auth
 ADD requirements.txt /excelplay/excelplay_auth/
 RUN pip install -r requirements.txt
 ADD . /excelplay/excelplay_auth
