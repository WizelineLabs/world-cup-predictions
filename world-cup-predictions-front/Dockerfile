FROM node:alpine
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

#ENV VITE_API_URL=https://worldcup-admin.wize.mx/api
ENV VITE_API_URL=http://localhost:8002/api
ENV VITE_GOOGLE_AUTH_KEY=117022430272-o9c3skq0riig5hf0ip8tbk9v8umuqepq.apps.googleusercontent.com
#ENV VITE_GOOGLE_AUTH_KEY=266500404779-69r7af0h79i0jck1l1vdsnjlqvs9i4s5.apps.googleusercontent.com
#ENV VITE_GOOGLE_AUTH_KEY=968240041302-2ktvmg3g7jtm1vnn064jmfcj24rhimee.apps.googleusercontent.com

COPY . /usr/src/app/

RUN npm install --legacy-peer-deps && npm run build

EXPOSE 8080

ENTRYPOINT ["npm", "start"]

