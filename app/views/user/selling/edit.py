from flask import redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm

from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, FileField, HiddenField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange

from app import bcrypt
from app.models.product import Product, Bid
from app.models.category import Category

import os

class EditView(MethodView):
    def get(self):
        form = EditForm()

        product = Product.objects(id=request.values["product_id"]).first()
        form.product_id.data = request.values["product_id"]
        form.price.data = product.price
        form.name.data = product.name
        form.detail.data=product.detail
        categories = Category.objects()

        return render_template('user/selling/edit.html', form=form, categories=categories,product=product)
    
    def post(self):
    
        form = EditForm()
        categories = Category.objects()
        product = Product.objects(id=form.product_id.data).first()

        if form.validate_on_submit() :
            product.name=form.name.data
            product.price=form.price.data
            product.detail=form.detail.data
            #product.image="product." + form.image.data.filename.split(".")[1].lower()
            #product.categories=request.form.getlist("categories")

            #image_path = os.path.join(os.getcwd(), 'app/static/image', str(product.id))
            #os.makedirs(image_path)
            #form.image.data.save(os.path.join(image_path, product.image))
            
            product.save()

            return redirect(url_for('user.selling_list'))
        
        return render_template('user/selling/edit.html', form=form, categories=categories, product=product)

class EditForm(FlaskForm):
    product_id = HiddenField("", validators=[InputRequired()])
    #image = FileField("商品照片", validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png', 'gif'], '只能上傳圖片(.jpg, .jpeg, .png, .gif)')])
    name = StringField("商品名稱", validators=[InputRequired("商品名稱不得為空"), Length(max=30, message="商品名稱不得超過30個字")])
    price = IntegerField("商品價格", validators=[InputRequired("商品價格不得為空"), NumberRange(min=1, max=100000, message="商品價格介於1~100000")])
    detail = CKEditorField("商品詳情")
    submit = SubmitField('上架')