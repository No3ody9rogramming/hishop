from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, HiddenField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange

from app.models.user import User, check_admin
from app.models.coupon import Coupon
import time

COUPON_STATUS = {"ACTIVE": 0, "NO_ACTIVE": 1, "ALL": 2}
class AdminCouponView(MethodView):
	def get(self):
		addForm = CouponForm()
		form = CouponManageForm()

		coupons = Coupon.objects()

		status = 2

		return render_template('admin/management/coupon.html', addForm=addForm, form=form, coupons=coupons, status=status, COUPON_STATUS=COUPON_STATUS)

	def post(self):
		addForm = CouponForm()
		form = CouponManageForm()
		coupons = Coupon.objects()

		status = 2
		if addForm.validate_on_submit():
			coupon = Coupon(title=addForm.title.data, detail=addForm.detail.data, discount=addForm.discount.data,
						 begin_time=addForm.begin_time.data, due_time=addForm.due_time.data)

			coupon.save()
		'''
		form = CouponManageForm()

		if form.validate_on_submit():
			user = User.objects(id=form.user_id.data, status__in=[ACCOUNT_STATUS["ACTIVE"], ACCOUNT_STATUS["LOCK"]]).first()
			if user.status == ACCOUNT_STATUS["ACTIVE"]:
				user.status = ACCOUNT_STATUS["LOCK"]
				print(user.to_json())
				user.save()
				return "解凍"
			elif user.status == ACCOUNT_STATUS["LOCK"]:
				user.status = ACCOUNT_STATUS["ACTIVE"]
				user.save()
				return "凍結"
		return "error"
		'''
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