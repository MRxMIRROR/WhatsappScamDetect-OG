# ------------ STAGE 1: Build React Frontend ------------
FROM node:20 AS frontend
WORKDIR /frontend

# Copy only files needed for build
COPY package*.json vite.config.ts tsconfig*.json postcss.config.js tailwind.config.js ./
COPY src ./src
COPY index.html ./

RUN npm ci
RUN npm run build


# ------------ STAGE 2: Python Backend ------------
FROM python:3.11-slim

WORKDIR /app
COPY ml_system ./ml_system
COPY --from=frontend /frontend/dist ./static

# Install dependencies
RUN pip install --no-cache-dir -r ml_system/requirements.txt

# EasyPanel injects $PORT automatically
ENV PORT=8080
EXPOSE 8080

# Start the Flask API (which will serve /static frontend files too)
CMD ["python", "ml_system/api.py"]
