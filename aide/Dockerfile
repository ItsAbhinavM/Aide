FROM rust:1.80-alpine AS base
RUN apk add --no-cache nodejs npm libc-dev

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
EXPOSE 1420
CMD [ "npm", "run", "tauri", "dev"]