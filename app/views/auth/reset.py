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
            return render_template('auth/reset.html', form=form, reset_token=reset_token, email=request.args.get('email'))
        else:
            return redirect(url_for('profile'))
    
    def post(self, reset_token):
        form = ResetPasswordForm()
        if form.validate_on_submit():
            if request.args.get('email') == None:
                flash('密碼修改失敗', 'danger')
                pass
            else:
                user = User.objects(email=request.args.get('email'), reset_token=reset_token).first()

                if user == None:
                    flash('密碼修改失敗', 'danger')
                    pass
                else:
                    user.reset_token = None
                    user.password = bcrypt.generate_password_hash(form.password.data).decode()
                    user.save()
                    flash('密碼修改成功', 'success')

        return render_template('auth/reset.html', form=form, reset_token=reset_token, email=request.args.get('email'))
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField("密碼", validators=[InputRequired(), Length(min=6,max=20)])
    confirm  = PasswordField("確認密碼", validators=[
        InputRequired(),
        Length(min=6,max=20),
        EqualTo('password', "Password must match")])
    submit = SubmitField('送出')