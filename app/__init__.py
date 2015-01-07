from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from md_renderer import md_renderer
import mistune

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
md = mistune.Markdown(renderer=md_renderer())

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from app import views, models, forms