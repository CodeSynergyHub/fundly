# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (e.g., for psycopg2 if you're using PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev build-essential gcc

# Install dependencies from requirements.txt
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the Django project code
COPY . /app/

# Expose the port the app runs on (e.g., 8000 for Django)
EXPOSE 8000

# Command to run Gunicorn and serve the Django application
# Dockerfile
ENTRYPOINT ["sh", "-c", "python manage.py migrate && exec gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
