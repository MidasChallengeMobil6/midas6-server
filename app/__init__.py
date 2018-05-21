from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
from app.model import *
db.create_all()

api_root = Api(app, catch_all_404s=True)

from app.api.v1 import *