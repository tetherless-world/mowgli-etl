# Build
FROM tiangolo/node-frontend:10 as build
WORKDIR /app
COPY /gui/gui .
RUN npm install
RUN npm run build

# Deployment
FROM nginx:1.17.10

RUN apt-get update && apt-get install -y curl

COPY /gui/gui/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
