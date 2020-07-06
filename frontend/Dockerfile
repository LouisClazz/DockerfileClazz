FROM node:lts-slim AS stage-build
WORKDIR /app
COPY package.json . 
COPY package-lock.json .
RUN npm ci
COPY . .
RUN npm run build


FROM nginx:1.17-alpine 
COPY --from=stage-build /app/dist /usr/share/nginx/html/

