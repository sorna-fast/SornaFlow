#!/bin/bash
set -e  

echo "Starting application..."


echo "Waiting for database to be ready..."
sleep 3


echo "Running database migrations..."
python manage.py migrate --noinput


echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000