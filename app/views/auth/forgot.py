from flask import redirect, render_template, url_for, request, abort
from flask.views import MethodView
from flask_login import login_user, current_user, login_required, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, ValidationError

from app import bcrypt, send_mail
from app.models.user import User

import uuid

class ForgotPasswordView(MethodView):
    def get(self):
        form = ForgotPasswordForm()
        if current_user.is_active == False:
            return render_template('auth/forgot.html', form=form, next=request.args.get('next'))
        else:
            return redirect(url_for('profile'))
    
    def post(self):
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            user = User.objects(account=form.account.data).first()
            user.reset_token = str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')
            user.save()

            send_mail("重設密碼", [user.email], url_for('forgot', _external=True) + "/" + user.reset_token + "?email=" + user.email)

        return render_template('auth/forgot.html', form=form)
    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    if user == None:
        raise ValidationError('此帳號尚未註冊')
        
class ForgotPasswordForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), validate_account])
    submit = SubmitField('送出')