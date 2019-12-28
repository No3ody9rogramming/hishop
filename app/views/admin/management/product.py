from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from wtforms import SubmitField, HiddenField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange

from app.models.user import User, check_admin
from app.models.product import Product
import time

PRODUCT_STATUS = {"SELLING" : 0, "SOLD" : 1, "FROZEN" : 2, "REMOVE" : 3, "ALL" : 4}
class ProductView(MethodView):
	def get(self):
		form = ManagementForm()

		
		if request.args.get("status") == str(PRODUCT_STATUS["SELLING"]):
			products = Product.objects(status__in=[PRODUCT_STATUS["SELLING"]])
			status = PRODUCT_STATUS["SELLING"]
		elif request.args.get("status") == str(PRODUCT_STATUS["SOLD"]):
			products = Product.objects(status__in=[PRODUCT_STATUS["SOLD"]])
			status = PRODUCT_STATUS["SOLD"]
		elif request.args.get("status") == str(PRODUCT_STATUS["FROZEN"]):
			products = Product.objects(status__in=[PRODUCT_STATUS["FROZEN"]])
			status = PRODUCT_STATUS["FROZEN"]
		elif request.args.get("status") == str(PRODUCT_STATUS["REMOVE"]):
			products = Product.objects(status__in=[PRODUCT_STATUS["REMOVE"]])
			status = PRODUCT_STATUS["REMOVE"]
		else:
			products = Product.objects(status__in=[PRODUCT_STATUS["SELLING"], PRODUCT_STATUS["SOLD"], PRODUCT_STATUS["FROZEN"], PRODUCT_STATUS["REMOVE"]])
			status = PRODUCT_STATUS["ALL"]

		return render_template('admin/management/product.html', form=form, status=status, products=products, PRODUCT_STATUS=PRODUCT_STATUS)

	def post(self):
		form = ManagementForm()

		if form.validate_on_submit():
			product = Product.objects(id=form.product_id.data).first()

			if product.status == PRODUCT_STATUS["SELLING"]:
				product.status = PRODUCT_STATUS["FROZEN"]
				product.save()
				return "解凍"
			elif product.status == PRODUCT_STATUS["FROZEN"]:
				product.status = PRODUCT_STATUS["SELLING"]
				product.save()
				return "凍結"
		return "hello"

		

class ManagementForm(FlaskForm):
    product_id = HiddenField("", validators=[InputRequired()])
    submit = SubmitField("")