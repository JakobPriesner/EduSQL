FROM node:alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN npm install -g @angular/cli

RUN npm install --force

EXPOSE 4200

CMD ["ng", "serve", "--host", "127.0.0.1"]