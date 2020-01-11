from flask import redirect, render_template, url_for, request, flash
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import SubmitField, PasswordField
from wtforms.validators import InputRequired, ValidationError, Length, EqualTo

from app import bcrypt
from app.models.user import User

class ResetPasswordView(MethodView):
    def get(self, reset_token):
        form = ResetPasswordForm()
        if current_user.is_active == False:
            return render_template('auth/reset.html', form=form, reset_token=reset_token, account=request.args.get('account'))
        else:
            return redirect(url_for('profile'))
    
    def post(self, reset_token):
        form = ResetPasswordForm()
        if form.validate_on_submit():
            if request.args.get('account') == None:
                flash('密碼修改失敗', 'error')
                pass
            else:
                user = User.objects(account=request.args.get('account'), reset_token=reset_token).first()

                if user == None:
                    flash('密碼修改失敗', 'danger')
                    pass
                else:
                    user.reset_token = None
                    user.password = bcrypt.generate_password_hash(form.password.data).decode()
                    user.save()
                    return redirect(url_for('login'))

        return render_template('auth/reset.html', form=form, reset_token=reset_token, account=request.args.get('account'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField("密碼", validators=[InputRequired("密碼不得為空"), Length(min=6,max=20, message="密碼介於6~20個字")])
    confirm  = PasswordField("確認密碼", validators=[
        InputRequired("確認密碼不得為空"),
        Length(min=6,max=20),
        EqualTo('password', "密碼前後不一致")])
    submit = SubmitField('送出')