from flask import request, redirect
from flask.views import MethodView
from flask_login import login_required, current_user, logout_user

class LogoutAPI(MethodView):
    @login_required
    def get(self):
        logout_user()
        print('123')
        return redirect('/login')