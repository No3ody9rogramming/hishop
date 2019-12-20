from flask import redirect, render_template, url_for, flash ,request
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError, Optional

from app.models.user import User

import os

class ProfileView(MethodView):
    def get(self):
        form = ProfileForm(name=current_user.name, birth=current_user.birth, phone=current_user.phone,
        store_name=current_user.store_name ,icon=current_user.icon, address=current_user.address, prefer_begin_time=current_user.prefer_begin_time, prefer_end_time=current_user.prefer_end_time)

        return render_template('user/account/profile.html', form=form)
    
    def post(self):
        form = ProfileForm()
        print(form.icon.data.filename)
        if form.validate_on_submit():
            print("valid")
            current_user.name = form.name.data
            current_user.phone = form.phone.data
            current_user.birth = form.birth.data
            current_user.store_name = form.store_name.data
            current_user.address = form.address.data
            current_user.prefer_begin_time = form.prefer_begin_time.data
            current_user.prefer_end_time = form.prefer_end_time.data
            
            if(form.icon.data.filename!=''):
                icon_path = os.path.join(os.getcwd(), 'app/static/icon', str(current_user.id))
                print(current_user.icon)
                if(current_user.icon == "default.png"):
                    os.makedirs(icon_path)
                else:
                    try:
                        os.remove(os.path.join(icon_path, current_user.icon))   #刪掉原本的檔案
                        print("File is deleted successfully")
                        
                    except:
                        print(e)
                current_user.icon = "icon." + form.icon.data.filename.split('.')[-1].lower()  #有上傳成功的話會是icon.xxx，否則為default.png
                form.icon.data.save(os.path.join(icon_path, current_user.icon)) #儲存上傳的檔案
            
            current_user.save()
            

            

        return render_template('user/account/profile.html', form=form)
        
class ProfileForm(FlaskForm):
    name = StringField("姓名", validators=[InputRequired(), Length(min=2, max=20)])
    store_name = StringField("賣場名稱", validators=[InputRequired(), Length(min=2, max=20)])
    icon = FileField("商品照片", validators=[Optional(), FileAllowed(['jpeg', 'jpg', 'png', 'gif'], '只能上傳圖片')])
    phone = StringField("電話號碼", validators=[InputRequired(), Length(max=15)])
    birth = DateField("生日", validators=[InputRequired()])
    address = StringField("地址", validators=[InputRequired(), Length(max=50)])
    prefer_begin_time = StringField("偏好起始時間", validators=[InputRequired(), Length(max=10)])
    prefer_end_time = StringField("偏好結束時間", validators=[InputRequired(), Length(max=10)])
    submit = SubmitField('修改')

