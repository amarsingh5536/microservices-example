#!/bin/bash
# export PORT=***

# Make migrations
# python manage.py makemigrations

# # Apply migrations
# python manage.py migrate

# Start the pubsub consumer in the background
service supervisor start

# Start the Django development server
python manage.py runserver 0.0.0.0:${PORT}
