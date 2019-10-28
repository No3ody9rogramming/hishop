from flask import redirect, render_template
from flask.views import MethodView
from flask_login import login_user, current_user, login_required, logout_user

from app.models.user import User
from app.forms.auth.login import LoginForm

class LoginAPI(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('auth/login.html', form=form)
    
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.objects(account=form.account.data).first()
            login_user(user)
        return render_template('auth/login.html', form=form)