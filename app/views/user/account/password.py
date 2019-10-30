from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import current_user

from app import bcrypt
from app.forms.user.account.password import PasswordForm

class PasswordView(MethodView):
    def get(self):
        form = PasswordForm()

        return render_template('user/account/password.html', form=form)
    
    def post(self):
        form = PasswordForm()
        if form.validate_on_submit():
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode()
            current_user.save()
            flash('修改成功')
        return redirect(url_for('password'))