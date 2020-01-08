from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

import uuid, json, requests, shelve, datetime

from app import app
from app.models.product import Product
from app.models.information import Information
from app.models.order import Order


class CartOperationView(MethodView):
    def get(self):
        coupons = list()
        temp_coupons = Information.objects(user_id=current_user.id).first().coupon

        now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        for temp_coupon in temp_coupons:
            if now > temp_coupon.begin_time and now < temp_coupon.due_time and Order.objects(buyer_id=current_user.id, coupon_id=temp_coupon.id).first() == None:
                coupons.append(temp_coupon.to_json())
        return json.dumps({'coupons': coupons})
    def post(self):
        product_id = request.values['product_id']
        product = Product.objects(id=product_id).first()

        if product == None:
            abort(404)
        information = Information.objects(user_id=current_user.id).first()
        for (idx, cart) in enumerate(information.cart):
            if product.id == cart.id:
                del information.cart[idx]
                information.save()
                return "加入購物車"

        information.cart.append(product.id)
        information.save()
        return "移出購物車"
        return abort(404);