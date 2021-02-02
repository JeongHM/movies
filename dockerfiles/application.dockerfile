FROM python:3.7-alpine3.11

WORKDIR /home

COPY . .

EXPOSE 5050

RUN pip3 install -r src/requirements.txt