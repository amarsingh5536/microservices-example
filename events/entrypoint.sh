#!/bin/bash
# export PORT=***

# Run database migrations
# flask db migrate
flask db upgrade

# Start the pubsub consumer in the background
service supervisor start
flask load_templates

# Start the Flask application
flask run --host=0.0.0.0 --port=${PORT}
