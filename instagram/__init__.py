from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager

app = Flask(__name__)                 # 初始化app对象

app.config.from_pyfile('app.conf')    # 设置app的配置文件
app.secret_key = 'instagram'          
login_manager = LoginManager(app)
login_manager.login_view = '/login/'   # 设置登陆路径

db=SQLAlchemy(app)                     

from instagram import models,views