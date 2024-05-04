FROM node:20-alpine as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

RUN npm run build

# stage 2 web server
FROM nginx:stable-alpine as production-stage

# WORKDIR /usr/share/nginx/html
# RUN rm -rf ./*

COPY --from=build-stage /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]