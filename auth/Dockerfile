FROM python:2.7.15
ADD requirements.txt /requirements.txt
WORKDIR /
RUN apt-get update
RUN apt-get install python-psycopg2 -y
RUN pip install psycopg2
RUN pip install -r requirements.txt