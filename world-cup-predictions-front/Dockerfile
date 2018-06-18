FROM node:carbon-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV API_URL=http://localhost:8002/api
ENV GOOGLE_AUTH_KEY=117022430272-o9c3skq0riig5hf0ip8tbk9v8umuqepq.apps.googleusercontent.com

COPY . /usr/src/app/
RUN npm install && npm run build

ENTRYPOINT ["npm", "start"]

