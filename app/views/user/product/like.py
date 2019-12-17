from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.product import Product
from app.models.information import Information

PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}
class LikeView(MethodView):
    def get(self):
        products = Information.objects(user_id=current_user.id).first().like

        return render_template('user/product/like.html', products=products,PRODUCT_STATUS=PRODUCT_STATUS)
    def post(self):
    	pass