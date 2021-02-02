FROM node:12.20.1-alpine3.9

WORKDIR /home

COPY ./swagger .

EXPOSE 3000

RUN npm install --silent