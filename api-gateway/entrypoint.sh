#!/bin/sh

# Ensure Python can find the app
export PYTHONPATH=$PYTHONPATH:/app

# Run uvicorn
exec uvicorn main:app --reload --host ${HOST} --port ${PORT}
