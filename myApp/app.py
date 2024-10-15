from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path



app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = "2cf09b58-e3a6-497f-a14c-c9ed405bcd91"

def mkpath(p):
    return os.path.normpath (
    os.path.join(
    os.path.dirname(__file__ ),
    p))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)

login_manager = LoginManager(app)