FROM node:lts-slim as build-stage

WORKDIR /app

ADD package-lock.json .

ADD package.json .

RUN npm ci

COPY . .

ARG BUILD_ENVIRONMENT=production

RUN npm run build -- --mode=${BUILD_ENVIRONMENT}

FROM nginx:1.17-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html/