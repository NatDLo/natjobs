# Stage 1: Build Angular frontend
FROM node:20-alpine AS builder

WORKDIR /app

COPY natjobs_frontend/package*.json ./
RUN npm ci

COPY natjobs_frontend/ .
RUN npm run build -- --configuration production

# Stage 2: Serve with Nginx
FROM nginx:alpine

COPY natjobs_frontend/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist/natjobs_frontend/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
