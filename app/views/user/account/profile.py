from flask import redirect, render_template, url_for, flash ,request
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.user import User

import os

class ProfileView(MethodView):
    def get(self):
        form = ProfileForm(name=current_user.name, birth=current_user.birth, phone=current_user.phone,
        store_name=current_user.store_name ,icon=current_user.icon)

        return render_template('user/account/profile.html', form=form)
    
    def post(self):
        form = ProfileForm()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.phone = form.phone.data
            current_user.birth = form.birth.data
            current_user.store_name = form.store_name.data
            icon="icon." + form.icon.data.filename[-3:].lower()
            current_user.save()

            icon_path = os.path.join(os.getcwd(), 'app/static/icon', str(current_user.id))
            os.makedirs(icon_path)
            form.icon.data.save(os.path.join(icon_path, current_user.icon))

        return redirect(url_for('profile'))
        
class ProfileForm(FlaskForm):
    name = StringField("姓名", validators=[InputRequired(), Length(min=2, max=20)])
    store_name = StringField("賣場名稱", validators=[InputRequired(), Length(min=2, max=20)])
    icon = FileField("商品照片", validators=[FileRequired(), FileAllowed(['jpg', 'png'], '只能上傳圖片')])
    phone = StringField("電話號碼", validators=[InputRequired(), Length(max=15)])
    birth = DateField("生日", validators=[InputRequired()])
    address = StringField("偏好地點",validators=[InputRequired(),Length(max=50)])
    begin = StringField("偏好時間(起)",validators=[InputRequired(),Length(max=10)])
    end = StringField("偏好時間(終)",validators=[InputRequired(),Length(max=10)])
    submit = SubmitField('修改')

