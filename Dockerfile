# ====================================================
# 1️⃣ Frontend Build Stage (React + Vite)
# ====================================================
FROM node:18 AS frontend

WORKDIR /frontend

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# ====================================================
# 2️⃣ Backend Stage (Flask API + ML Model)
# ====================================================
FROM python:3.10-slim AS backend

WORKDIR /app

# Copy backend files
COPY ml_system ./ml_system
COPY ml_system/requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend from first stage
COPY --from=frontend /frontend/dist ./frontend

# Expose backend port
EXPOSE 5000

# Train model if not already trained
RUN python ml_system/train.py --create-sample || true

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

CMD ["python", "ml_system/api.py"]
