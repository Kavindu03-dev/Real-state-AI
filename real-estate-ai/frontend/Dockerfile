# Frontend Dockerfile for Real Estate AI (Vite React)
# Build stage
FROM node:18-alpine AS build
WORKDIR /app

# Install deps
COPY package*.json ./
RUN npm ci || npm install

# Build
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:1.25-alpine AS runtime

# Copy custom nginx config (proxies /api -> backend service)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static assets
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
