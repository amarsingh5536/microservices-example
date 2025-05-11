import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import app_config
from dotenv import load_dotenv
load_dotenv()

api_version = 'v1'
build_version = "Build Version: 1.0"

# Get the environment mode from FLASK_ENV (default: 'development')
FLASK_ENV = os.getenv("FLASK_ENV", "development")

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config.get(FLASK_ENV, 'development'))

# configuration of mail
app.config['MAIL_SERVER'] = os.environ['EMAIL_HOST']
app.config['MAIL_PORT'] = os.environ['EMAIL_PORT']
app.config['MAIL_USERNAME'] = os.environ['EMAIL_HOST_USER']
app.config['MAIL_SENDER_ID'] = os.environ['EMAIL_SENDER_ID']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_HOST_PASSWORD']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

db = SQLAlchemy(app)

def get_app():
    migrate = Migrate(app, db, compare_type=True)
    from events_app import models
    from events_app import routes
    import fixture_loader
    return app
