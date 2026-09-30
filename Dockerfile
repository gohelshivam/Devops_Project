# Lightweight official Python base image
FROM python:3.12-slim

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    APP_VERSION="1.0.0"

# Container ke andar working directory
WORKDIR /app

# Sabse pehle requirements copy aur install (Layer caching ke liye)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pura application code copy karein
COPY . .

# Port expose karein
EXPOSE 5000

# Container healthcheck instruction
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Production WSGI server Gunicorn run karein
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
