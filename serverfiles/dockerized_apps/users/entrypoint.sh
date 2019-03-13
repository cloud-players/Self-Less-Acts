#!/bin/sh

# Collect static files
echo "Running with hostname"
echo $HOSTNAME 

# Apply database migrations
echo "Applying database migrations"
python3 users/manage.py makemigrations
python3 users/manage.py migrate

# Start server
echo "Starting server"
python3 users/manage.py runserver 0:80