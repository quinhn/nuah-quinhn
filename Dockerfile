FROM python:3

RUN mkdir /app/
ADD . /app/
WORKDIR /app
RUN pip install -r requirement.txt
