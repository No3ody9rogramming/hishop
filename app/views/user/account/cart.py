from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import BooleanField, SubmitField, FieldList, SelectField
from wtforms.validators import InputRequired, NumberRange

from bson.objectid import ObjectId
import uuid, json, requests, shelve

from app import app
from app.models.payment import Payment
from app.models.information import Information
from app.models.product import Product
from app.models.order import Order, ORDER_STATUS
from app.models.coupon import Coupon, COUPON_STATUS

class CartView(MethodView):
    def get(self):
        form = CartForm()
        products = Information.objects(user_id=current_user.id).first().cart

        coupons = list(Information.objects(user_id=current_user.id).first().coupon)
        for i in range(len(coupons) - 1, -1, -1):
            if coupons[i].status == COUPON_STATUS["EXPIRED"] or Order.objects(buyer_id=current_user.id, coupon_id=coupons[i].id, status__ne=ORDER_STATUS["CANCEL"]).first() != None:
                del coupons[i]

        return render_template('user/account/cart.html', form=form, hicoin=current_user.hicoin, coupons=coupons, products = products)
    
    def post(self):
        form = CartForm()
        checkedProducts = request.form.getlist("productCheck")
        
        information = Information.objects(user_id=current_user.id).first()
        products = Product.objects(id__in=checkedProducts, seller_id__ne=current_user.id, status=0, bidding=False)
        total_price = 0
        coupon_dict = dict()
        for product in products:
            try:
                coupon = Coupon.objects(id=request.form.get(str(product.id))).first()
            except:
                coupon = None
            if coupon in information.coupon and Order.objects(buyer_id=current_user.id, coupon_id=coupon.id, status__ne=ORDER_STATUS["CANCEL"]).first() == None:
                total_price += max(0, int(product.price * product.discount - coupon.discount))
                coupon_dict[product.id] = coupon.id
            else:
                total_price += int(product.price * product.discount)
                coupon_dict[product.id] = None

        
        if current_user.hicoin >= total_price:
            current_user.hicoin -= total_price
            current_user.save()
            for product in products:
                Order(buyer_id=current_user.id, product_id=product.id, coupon_id=coupon_dict[product.id]).save()
                product.status = 1
                product.save()
                information.cart.remove(product)
                information.save()

        return redirect(url_for('user.purchase_list', status='4'));

class CartForm(FlaskForm):
    submit = SubmitField('確定結帳')