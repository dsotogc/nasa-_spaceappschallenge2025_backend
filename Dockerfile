# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar código
COPY . .

# expone puerto 80 (Fargate/ALB) o 8000 si prefieres
ENV PORT=80
EXPOSE 80

# comando para arrancar uvicorn en producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]