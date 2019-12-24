from flask import request, redirect, url_for, abort
from flask.views import MethodView
from flask_login import login_required, current_user, login_user

from app.models.user import User

class VerificationView(MethodView):
    def get(self, user_id):
    	user = User.objects(id=user_id).first()

    	if user != None:
    		user.status = 1
    		user.save()
    		login_user(user)

    		return redirect(url_for('index'))

    	abort(404)