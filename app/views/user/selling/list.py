from flask import redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.order import Order
from app.models.product import Product

from wtforms.validators import InputRequired
from wtforms import SubmitField, HiddenField
from flask_wtf import FlaskForm

import datetime

#移交中 領收中 已完成 已取消 全部
PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}
class SellingListView(MethodView):
    def get(self):
        form = SellingListForm()
        products = Product.objects(seller_id=current_user.id)

        status = request.args.get('status')
        if status == PRODUCT_STATUS['SELLING']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['SELLING'])
        elif status == PRODUCT_STATUS['FROZEN']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['FROZEN'])
        elif status == PRODUCT_STATUS['REMOVE']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['REMOVE'])
        else:
            status = PRODUCT_STATUS["ALL"]
            products = Product.objects(seller_id=current_user.id, status__ne=PRODUCT_STATUS['SOLD'])

        products = sorted(products, key=lambda k: k.create_time, reverse=False)

        return render_template('user/selling/list.html', products=products, PRODUCT_STATUS=PRODUCT_STATUS, status=status, form=form)
    def post(self):
        form = SellingListForm()
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
        #print(request.values['ProductID'])
        if form.validate_on_submit:
            #print(request.values['ProductID'])
            product = Product.objects(id=form.product_id.data).first()
            product.status = PRODUCT_STATUS['REMOVE']
            product.save()
            


        products = Product.objects(seller_id=current_user.id)

        status = request.args.get('status')
        if status == PRODUCT_STATUS['SELLING']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['SELLING'])
        elif status == PRODUCT_STATUS['FROZEN']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['FROZEN'])
        elif status == PRODUCT_STATUS['REMOVE']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['REMOVE'])
        else:
            status = PRODUCT_STATUS["ALL"]
            products = Product.objects(seller_id=current_user.id, status__ne=PRODUCT_STATUS['SOLD'])

        products = sorted(products, key=lambda k: k.create_time, reverse=False)

        return render_template('user/selling/list.html', products=products, PRODUCT_STATUS=PRODUCT_STATUS, status=status, form=form)
class SellingListForm(FlaskForm):
    product_id = HiddenField("", validators=[InputRequired()])
    remove = SubmitField('下架此商品')
    edit = SubmitField('編輯商品')