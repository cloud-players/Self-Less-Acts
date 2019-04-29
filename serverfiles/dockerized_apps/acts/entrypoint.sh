#!/bin/sh

# Collect static files
#echo "Running with hostname"
#echo $HOSTNAME 

# Apply database migrations
#echo "Applying database migrations"
#python3 acts/manage.py makemigrations
#python3 acts/manage.py migrate

# Start server
echo "Starting server"
python3 acts/manage.py runserver 0:80
