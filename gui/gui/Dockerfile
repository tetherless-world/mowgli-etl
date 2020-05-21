# Build
FROM tiangolo/node-frontend:10 as build
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Deployment
FROM nginx:1.17.6

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
