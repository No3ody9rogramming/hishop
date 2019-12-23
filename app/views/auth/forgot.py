from flask import redirect, render_template, url_for, request, flash
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from app import bcrypt, send_mail
from app.models.user import User

import uuid

class ForgotPasswordView(MethodView):
    def get(self):
        form = ForgotPasswordForm()
        '''if current_user.is_active == False:
            return render_template('auth/forgot.html', form=form)
        else:
            return redirect(url_for('profile'))'''
        if current_user.is_anonymous == True:
            return render_template('auth/forgot.html', form=form)
        else:
            return redirect(url_for('user.profile'))
    
    def post(self):
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            user = User.objects(account=form.account.data).first()
            user.reset_token = str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')
            user.save()

            send_mail("重設密碼", [user.email], url_for('reset', reset_token=user.reset_token, email=user.email, _external=True))

            flash('重設密碼連結已發送', category='success')

        return render_template('auth/forgot.html', form=form)
    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    if user == None:
        raise ValidationError('此帳號尚未註冊')
        
class ForgotPasswordForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), validate_account])
    submit = SubmitField('送出')