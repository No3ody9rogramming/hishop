from flask import redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.order import Order
from app.models.product import Product

import datetime

#移交中 領收中 已完成 已取消 全部
PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}
class SellingListView(MethodView):
    def get(self):
        products = Product.objects(seller_id=current_user.id)

        status = request.args.get('status')
        if request.args.get('status') == PRODUCT_STATUS['SELLING']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['SELLING'])
        elif request.args.get('status') == PRODUCT_STATUS['FROZEN']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['FROZEN'])
        elif request.args.get('status') == PRODUCT_STATUS['REMOVE']:
            products = Product.objects(seller_id=current_user.id, status=PRODUCT_STATUS['REMOVE'])
        else:
            status = PRODUCT_STATUS["ALL"]
            products = Product.objects(seller_id=current_user.id, status__ne=PRODUCT_STATUS['SOLD'])

        products = sorted(products, key=lambda k: k.create_time, reverse=False)

        return render_template('user/selling/list.html', products=products, PRODUCT_STATUS=PRODUCT_STATUS, status=status)
    def post(self):
        pass