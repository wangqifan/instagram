from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager

app = Flask(__name__)

app.config.from_pyfile('app.conf')
app.secret_key = 'instagram'
login_manager = LoginManager(app)
login_manager.login_view = '/login/'

db=SQLAlchemy(app)

from instagram import models,views