from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import UserMixin, LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_mail import Mail, Message
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix
from threading import Thread, Lock
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

async_mode = "threading"

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
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def send_mail(title, recipients, body):
	msg = Message(title, sender="HiShop", recipients=recipients)
	msg.body = body

	mail.send(msg)
	t = Thread(target=send_async_email, args=[app, msg])
	t.start()

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)