from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import UserMixin, LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('../config.cfg')

login_manager = LoginManager(app)
login_manager.login_view = "login_view"
db = MongoEngine(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)