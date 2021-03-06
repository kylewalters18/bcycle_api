import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# Ideally use Nginx for CORS and gzip compression
# Not sure if possible with Heroku deployment
Compress(app)
CORS(app, origins=['*'])

db = SQLAlchemy(app)

from bcycle.v1 import v1_blueprint
app.register_blueprint(v1_blueprint, url_prefix='/v1')

from bcycle import errors
