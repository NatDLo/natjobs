FROM python:3.8-slim

WORKDIR /app

# Install system dependencies for psycopg2 and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from root requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

EXPOSE 8000

# Run migrations, collectstatic and launch Daphne ASGI server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p 8000 backend.asgi:application"]
