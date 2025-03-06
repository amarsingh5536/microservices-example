import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config
from dotenv import load_dotenv
load_dotenv()

api_version = 'v1'
build_version = "Build Version: 1.0"

# Get the environment mode from FLASK_ENV (default: 'development')
FLASK_ENV = os.getenv("FLASK_ENV", "development")

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config.get(FLASK_ENV, 'development'))

db = SQLAlchemy(app)

def get_app():
    migrate = Migrate(app, db, compare_type=True)
    from events_app import models
    from events_app import routes
    return app
