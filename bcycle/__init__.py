import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
CORS(app, origins=['*'])

db = SQLAlchemy(app)

from bcycle import endpoints
from bcycle import models
