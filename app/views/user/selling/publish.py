from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm

from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, RadioField, FileField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange

from app import bcrypt
from app.models.product import Product, Bid
from app.models.catogory import Catogory

import os

class PublishView(MethodView):
    def get(self):
        form = PublishForm()
        return render_template('user/selling/publish.html', form=form)
    
    def post(self):
        form = PublishForm()
        if form.validate_on_submit():
            product = Product(seller_id=current_user.id,
                              name=form.name.data,
                              price=form.price.data,
                              detail=form.detail.data,
                              image="product." + form.image.data.filename[-3:].lower(),
                              auction=bool(form.auction.data),
                              status=0)
            product.save()

            image_path = os.path.join(os.getcwd(), 'app\\static\\image', str(product.id))
            os.makedirs(image_path)
            form.image.data.save(os.path.join(image_path, product.image))

            if product.auction == True:
                bid = Bid(per_price=form.per_price.data,
                          low_price=form.low_price.data,
                          due_time=form.due_time.data)
                product.bid = bid
                product.save()

            return redirect(url_for('profile'))
        
        return render_template('user/selling/publish.html', form=form)
        
class PublishForm(FlaskForm):
    image = FileField("商品照片", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], '只能上傳圖片')])
    name = StringField("商品名稱", validators=[InputRequired(), Length(max=50)])
    price = IntegerField("商品直購價", validators=[InputRequired(), NumberRange(min=1, max=100000)])
    low_price = IntegerField("起標價", validators=[InputRequired(), NumberRange(min=1, max=10000)])
    per_price = IntegerField("每刀價格", validators=[InputRequired(), NumberRange(min=1, max=1000)])
    due_time = DateTimeLocalField("截標時間", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    auction = RadioField('radio', coerce=int, choices=[(0,'定價販售'),(1,'競標販售')], validators=[InputRequired()])
    detail = CKEditorField("商品詳情")
    submit = SubmitField('上架')