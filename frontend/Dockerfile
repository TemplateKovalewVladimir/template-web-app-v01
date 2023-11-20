# Этап сборки (build stage)
FROM node:20 as build-stage

WORKDIR /app

COPY ./package*.json ./
RUN npm install

COPY ./ ./
RUN npm run build

# Этап production (production-stage)
FROM nginx:1.25.3-alpine3.18 as production-stage

ENV TZ=Europe/Moscow
RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]