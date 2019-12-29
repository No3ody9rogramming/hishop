from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from app import bcrypt

class PasswordView(MethodView):
    def get(self):
        form = PasswordForm()

        return render_template('user/account/password.html', form=form)
    def post(self):
        form = PasswordForm()
        if form.validate_on_submit():
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode()
            current_user.save()
            flash('修改成功', 'success')

            return redirect(url_for('user.password'))
        return render_template('user/account/password.html', form=form)



def validate_old_password(form, oldPassword):
    if bcrypt.check_password_hash(current_user.password, oldPassword.data) == False:
        raise ValidationError('密碼錯誤')

class PasswordForm(FlaskForm):
    old_password = PasswordField("舊密碼", validators=[InputRequired("舊密碼不得為空"), validate_old_password])
    password = PasswordField("新密碼", validators=[InputRequired("新密碼不得為空"), Length(min=6,max=20,message="密碼介於6~20個字")])
    confirm  = PasswordField("確認新密碼", validators=[
        InputRequired("確認新密碼不得為空"),
        EqualTo('password', "密碼前後不一致")])
    submit = SubmitField('確認')