from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_user

from app import bcrypt
from app.forms.auth.register import RegisterForm
from app.models.user import User

class RegisterView(MethodView):
    def get(self):
        form = RegisterForm()
        return render_template('auth/register.html', form=form)
    
    def post(self):
        form = RegisterForm()
        
        if form.validate_on_submit():
            user = User(name=form.name.data,
                        account=form.account.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode(),
                        phone=form.phone.data)
            user.save()
            login_user(user)
            return redirect(url_for('profile'))
        
        return render_template('auth/register.html', form=form)