from flask import redirect, render_template, url_for, flash ,request
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.user import User


class ProfileView(MethodView):
    def get(self):
        form = ProfileForm(name=current_user.name, birth=current_user.birth, phone=current_user.phone,
        store_name=current_user.store_name )

        return render_template('user/account/profile.html', form=form)
    
    def post(self):
        form = ProfileForm()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.phone = form.phone.data
            current_user.birth = form.birth.data
            current_user.store_name = form.store_name.data
            current_user.save()
        return redirect(url_for('profile'))
        
class ProfileForm(FlaskForm):
    name = StringField("姓名", validators=[InputRequired(), Length(min=2, max=20)])
    store_name = StringField("賣場名稱", validators=[InputRequired(), Length(min=2, max=20)])
    phone = StringField("電話號碼", validators=[InputRequired(), Length(max=15)])
    birth = DateField("生日", validators=[InputRequired()])
    address = StringField("偏好地點",validators=[InputRequired(),Length(max=50)])
    begin = StringField("偏好時間(起)",validators=[InputRequired(),Length(max=10)])
    end = StringField("偏好時間(終)",validators=[InputRequired(),Length(max=10)])
    submit = SubmitField('修改')

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def create_uuid(self): #生成唯一的圖片的名稱字串，使用使用者id為uuid
    return current_user.id