from flask import request, redirect, url_for
from flask.views import MethodView
from flask_login import login_required, current_user, logout_user

class LogoutView(MethodView):
    def get(self):
        logout_user()
        #return redirect('/login')
        return redirect(url_for('login'))