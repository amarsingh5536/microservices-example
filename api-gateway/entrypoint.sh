#!/bin/sh

# Ensure Python can find the app
export PYTHONPATH=$PYTHONPATH:/app

# Run uvicorn
exec uvicorn main:app --reload --host 0.0.0.0 --port ${PORT}
