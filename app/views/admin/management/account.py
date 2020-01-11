from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from wtforms import SubmitField, HiddenField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange

from app.models.user import User, check_admin
from app.models.product import Product, PRODUCT_STATUS
from app.models.order import Order, ORDER_STATUS
import time

ACCOUNT_STATUS = {"NO_ACTIVE": 0, "ACTIVE" : 1, "LOCK": 3, "ALL": 4}
class AccountView(MethodView):
	def get(self):
		form = ManagementForm()

		if request.args.get("status") == str(ACCOUNT_STATUS["ACTIVE"]):
			users = User.objects(status__in=[ACCOUNT_STATUS["ACTIVE"]])
			status = ACCOUNT_STATUS["ACTIVE"]
		elif request.args.get("status") == str(ACCOUNT_STATUS["NO_ACTIVE"]):
			users = User.objects(status__in=[ACCOUNT_STATUS["NO_ACTIVE"]])
			status = ACCOUNT_STATUS["NO_ACTIVE"]
		elif request.args.get("status") == str(ACCOUNT_STATUS["LOCK"]):
			users = User.objects(status__in=[ACCOUNT_STATUS["LOCK"]])
			status = ACCOUNT_STATUS["LOCK"]
		else:
			users = User.objects(status__in=[ACCOUNT_STATUS["ACTIVE"], ACCOUNT_STATUS["NO_ACTIVE"], ACCOUNT_STATUS["LOCK"]])
			status = ACCOUNT_STATUS["ALL"]

		for user in users:
			user.products = len(Product.objects(seller_id=user.id, status=PRODUCT_STATUS["FROZEN"]))

		return render_template('admin/management/account.html', form=form, users=users, status=status, ACCOUNT_STATUS=ACCOUNT_STATUS)

	def post(self):
		form = ManagementForm()

		if form.validate_on_submit():
			user = User.objects(id=form.user_id.data, status__in=[ACCOUNT_STATUS["ACTIVE"], ACCOUNT_STATUS["LOCK"]]).first()
			if user.status == ACCOUNT_STATUS["ACTIVE"]:
				user.status = ACCOUNT_STATUS["LOCK"]
				orders = Order.objects(product_id__in=Product.objects(seller_id=form.user_id.data),
					 status__in=[int(ORDER_STATUS["TRANSFERING"]), int(ORDER_STATUS["RECEIPTING"])])
				for order in orders:
					if order.product_id.bidding == False:
						if order.coupon_id == None:
							order.buyer_id.hicoin += order.product_id.price
						else:
							order.buyer_id.hicoin += max(0, order.product_id.price - order.coupon_id.discount)
					else:
						order.buyer_id.hicoin += order.product_id.bid.now_price
					order.product_id.status = PRODUCT_STATUS["REMOVE"]
					order.status = int(ORDER_STATUS["CANCEL"])
					order.product_id.save()
					order.buyer_id.save()
					order.save()
				normal_products = Product.objects(seller_id=form.user_id.data, bidding=False, status__ne=PRODUCT_STATUS["FROZEN"])
				for product in normal_products:
					product.status = PRODUCT_STATUS["REMOVE"]
					product.save()
				bidding_product = Product.objects(seller_id=form.user_id.data, bidding=True, bid__buyer_id__ne=None)
				for product in bidding_product:
					product.status = PRODUCT_STATUS["REMOVE"]
					if product.bid.buyer_id == None:
						pass
					else:
						product.bid.buyer_id.hicoin += product.bid.now_price
					product.save()
				user.save()
				return "解凍"
			elif user.status == ACCOUNT_STATUS["LOCK"]:
				user.status = ACCOUNT_STATUS["ACTIVE"]
				user.save()
				return "凍結"
		return "error"

class ManagementForm(FlaskForm):
    user_id = HiddenField("", validators=[InputRequired()])
    submit = SubmitField("")