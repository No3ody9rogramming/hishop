from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import UserMixin, LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix

app = Flask(__name__)
app.config.from_pyfile('../config.cfg')

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = MongoEngine(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)
mail = Mail(app)
ReverseProxyPrefixFix(app)