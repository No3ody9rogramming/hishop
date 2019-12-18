from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.product import Product
from app.models.information import Information

PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}
SORT_STATUS = {"PRICE":"0","HOT":"1","RATING":"2","CREATE_TIME":"3"}
class HistoryView(MethodView):
    def get(self):
        products = Information.objects(user_id=current_user.id).first().history
        status = request.args.get('status')
        if(status == SORT_STATUS["CREATE_TIME"]):
            products = sorted(products, key=lambda k: k.create_time, reverse=False)
        elif(status == SORT_STATUS["PRICE"]):
            products = sorted(products, key=lambda k: k.product.price, reverse=False)
        elif(status == SORT_STATUS["HOT"]):
            products = sorted(products, key=lambda k: k.product.view, reverse=False)
        elif(status == SORT_STATUS["RATING"]):
            products = sorted(products, key=lambda k: k.product.seller_id.rating, reverse=False)
        

        return render_template('user/product/history.html', products=products,PRODUCT_STATUS=PRODUCT_STATUS,SORT_STATUS=SORT_STATUS)
    def post(self):
    	pass