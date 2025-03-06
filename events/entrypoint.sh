#!/bin/bash
# export PORT=***

# flask db migrate
flask db upgrade
flask run --host=0.0.0.0 --port=${PORT}