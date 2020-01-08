from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, HiddenField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange

from app.models.user import User, check_admin
from app.models.coupon import Coupon, COUPON_STATUS
import datetime
import time

class AdminCouponView(MethodView):
	def get(self):
		addForm = CouponForm()
		form = CouponManageForm()

		coupons = Coupon.objects()
		status = COUPON_STATUS["ALL"]
		if request.args.get("status") == str(COUPON_STATUS["ACTIVE"]):
			coupons = Coupon.objects(status=COUPON_STATUS["ACTIVE"])
			status = COUPON_STATUS["ACTIVE"]
		elif request.args.get("status") == str(COUPON_STATUS["NO_ACTIVE"]):
			coupons = Coupon.objects(status=COUPON_STATUS["NO_ACTIVE"])
			status = COUPON_STATUS["NO_ACTIVE"]
		elif request.args.get("status") == str(COUPON_STATUS["EXPIRED"]):
			coupons = Coupon.objects(status=COUPON_STATUS["EXPIRED"])
			status = COUPON_STATUS["EXPIRED"]

		return render_template('admin/management/coupon.html', addForm=addForm, form=form, coupons=coupons, status=status, COUPON_STATUS=COUPON_STATUS)

	def post(self):
		addForm = CouponForm()
		form = CouponManageForm()

		coupons = Coupon.objects()
		status = COUPON_STATUS["ALL"]
		if request.args.get("status") == str(COUPON_STATUS["ACTIVE"]):
			coupons = Coupon.objects(status=COUPON_STATUS["ACTIVE"])
			status = COUPON_STATUS["ACTIVE"]
		elif request.args.get("status") == str(COUPON_STATUS["NO_ACTIVE"]):
			coupons = Coupon.objects(status=COUPON_STATUS["NO_ACTIVE"])
			status = COUPON_STATUS["NO_ACTIVE"]
		elif request.args.get("status") == str(COUPON_STATUS["EXPIRED"]):
			coupons = Coupon.objects(status=COUPON_STATUS["EXPIRED"])
			status = COUPON_STATUS["EXPIRED"]

		
		if addForm.validate_on_submit():
			coupon = Coupon(title=addForm.title.data, detail=addForm.detail.data, discount=addForm.discount.data,
						 begin_time=addForm.begin_time.data, due_time=addForm.due_time.data)
			coupon.save()
			return redirect(url_for("admin.coupon"))

		if form.validate_on_submit():
			coupon = Coupon.objects(id=form.coupon_id.data, due_time__gte=datetime.datetime.utcnow()+datetime.timedelta(hours=8)).first()

			if coupon == None:
				return "error"
			elif coupon.status == COUPON_STATUS["ACTIVE"]:
				coupon.status = COUPON_STATUS["NO_ACTIVE"]
				coupon.save()
				return "發放"
			elif coupon.status == COUPON_STATUS["NO_ACTIVE"]:
				coupon.status = COUPON_STATUS["ACTIVE"]
				coupon.save()
				return "停發"
			else:
				return "error"

		return render_template('admin/management/coupon.html', addForm=addForm, form=form, coupons=coupons, status=status, COUPON_STATUS=COUPON_STATUS)

class CouponForm(FlaskForm):
	title = StringField("標題", validators=[InputRequired(), Length(max=20, message="標題不得超過20個字")])
	detail = StringField("描述", validators=[InputRequired(), Length(max=40000, message="描述不得超過40000字")])
	discount = IntegerField("折扣金額", validators=[InputRequired()])
	begin_time = DateField('開始時間', validators=[InputRequired()])
	due_time = DateField('結束時間', validators=[InputRequired()])
	submit = SubmitField("新增")

class CouponManageForm(FlaskForm):
	coupon_id = HiddenField("", validators=[InputRequired()])
	submit = SubmitField("")