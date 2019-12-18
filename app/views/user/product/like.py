from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.product import Product
from app.models.information import Information

PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}
SORT_STATUS = {"PRICE":"0","HOT":"1","RATING":"2","CREATE_TIME":"3"}
class LikeView(MethodView):
    def get(self):
        status = request.args.get('status')
        products = Information.objects(user_id=current_user.id).order_by(status).first().like

        return render_template('user/product/like.html', products=products,PRODUCT_STATUS=PRODUCT_STATUS,SORT_STATUS=SORT_STATUS)
    def post(self):
    	pass