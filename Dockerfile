FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8001
ENV PORT=8001

CMD ["sh", "-c", "gunicorn dashboard_project.wsgi:application --bind 0.0.0.0:${PORT}"]
