from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('API.config')
db = SQLAlchemy(app)

from API.app import views  #,models
