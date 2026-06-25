# syntax=docker/dockerfile:1
FROM node:22-bookworm-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --legacy-peer-deps
COPY . .
ARG STRAPI_URL
ARG STRAPI_TOKEN
ARG PUBLIC_FORMS_WEBHOOK
ENV STRAPI_URL=$STRAPI_URL STRAPI_TOKEN=$STRAPI_TOKEN PUBLIC_FORMS_WEBHOOK=$PUBLIC_FORMS_WEBHOOK
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
