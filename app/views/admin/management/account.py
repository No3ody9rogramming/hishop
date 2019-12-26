from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.user import User

ACCOUNT_STATUS = {"NO_ACITVE": "0", "ACTIVE" : "1", "LOCK": "3", "ALL": "4"}
class AccountView(MethodView):
	def get(self):
		

		users = User.objects(status__in=[0, 1])

		return users.to_json()

	def post(self):
		pass