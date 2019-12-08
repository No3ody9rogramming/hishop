from flask import request, redirect, url_for
from flask.views import MethodView
from flask_login import login_required, current_user, logout_user

class LogoutView(MethodView):
    def get(self):
        logout_user()

        if request.args.get('next'):
        	return redirect(request.args.get('next'))
        else:
        	return redirect(url_for('login'))