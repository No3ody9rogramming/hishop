from flask import redirect, render_template, url_for, flash ,request
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError, Optional

from app.models.user import User
from app.models.order import Order
from app.models.product import Product

import os
#移交中 領收中 已完成 已取消 全部
ORDER_STATUS = {"TRANSFERING" : "0", "RECEIPTING" : "1", "COMPLETE" : "2", "CANCEL" : "3", "ALL" : "4"}
class ProfileView(MethodView):
    def get(self):
        form = ProfileForm(name=current_user.name, birth=current_user.birth, phone=current_user.phone,
        store_name=current_user.store_name ,icon=current_user.icon, address=current_user.address, prefer_begin_time=current_user.prefer_begin_time, prefer_end_time=current_user.prefer_end_time)
        
        seller_orders = Order.objects(product_id__in=Product.objects(seller_id=current_user.id),status=ORDER_STATUS["COMPLETE"])
        buyer_orders = Order.objects(product_id__in=Product.objects(seller_id=current_user.id),status=ORDER_STATUS["COMPLETE"])
        rating = 0
        count_seller_orders = 0
        count_buyer_orders = 0
        for order in seller_orders:
            print(order.seller_rating)
            if order.seller_rating != None:
                rating += order.seller_rating
                count_seller_orders += 1
            
        for order in buyer_orders:
            print(order.buyer_rating)
            if order.buyer_rating!= None:
                rating += order.buyer_rating
                count_buyer_orders += 1
            #rating += buyer_orders.buyer_rating

        if(count_buyer_orders + count_seller_orders!=0):
            rating /= count_buyer_orders + count_seller_orders
        else:
            rating = 0


        print(rating)

        return render_template('user/account/profile.html', form=form,rating=rating)
    
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
            
            flash('修改成功', 'success')
            
            

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

