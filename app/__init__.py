from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import sqlite3 as sql

MyApp = Flask(__name__)
MyApp.config.from_object(Config)
MyDb = SQLAlchemy(MyApp)
migrate = Migrate(MyApp, MyDb)
login = LoginManager(MyApp)
login.login_view = 'login'

from app import routes, models