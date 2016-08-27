import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
CORS(app)

db = SQLAlchemy(app)

from bcycle import views
from bcycle import models
