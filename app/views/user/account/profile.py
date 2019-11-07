from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.user import User

class ProfileView(MethodView):
    def get(self):
        form = ProfileForm(name=current_user.name, born=current_user.born, phone=current_user.phone)

        return render_template('user/account/profile.html', form=form)
    
    def post(self):
        form = ProfileForm()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.phone = form.phone.data
            current_user.born = form.born.data
            current_user.save()
            flash('修改成功')
        return redirect(url_for('profile'))
        
class ProfileForm(FlaskForm):
    name = StringField("名稱", validators=[InputRequired(), Length(max=50)])
    phone = StringField("電話號碼", validators=[InputRequired(), Length(max=15)])
    born = DateField("出生日期", validators=[InputRequired()])
    submit = SubmitField('修改')