from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError

from wtforms import SubmitField, HiddenField
from app.models.information import Information
from app.models.coupon import Coupon, COUPON_STATUS

from bson.objectid import ObjectId
import datetime

class CouponView(MethodView):
    def get(self):
        form = CouponForm()
        if request.args.get('status') == str(COUPON_STATUS["ALL"]):
            coupons = Information.objects(user_id=current_user.id).first().coupon
            status = COUPON_STATUS["ALL"]
        else:
            coupons = Coupon.objects(id__nin=[coupon.id for coupon in Information.objects(user_id=current_user.id).first().coupon],
                begin_time__lte=datetime.datetime.utcnow()+datetime.timedelta(hours=8), status=COUPON_STATUS["ACTIVE"])
            status = None

        return render_template('user/coupon/list.html', status=status, coupons=coupons, form=form, COUPON_STATUS=COUPON_STATUS)
    def post(self):
        form = CouponForm()

        if form.validate_on_submit():
            information = Information.objects(user_id=current_user.id).first()
            coupon = Coupon.objects(id=form.coupon_id.data).first()
            information.coupon.append(coupon)
            information.save()

            return redirect(url_for('user.coupon', status=COUPON_STATUS["ALL"]))

        return self.get()

def validate_coupon(form, coupon_id):
    coupon = Coupon.objects(id=coupon_id.data, begin_time__lte=datetime.datetime.utcnow()+datetime.timedelta(hours=8), status=COUPON_STATUS["ACTIVE"]).first()

    if coupon == None:
        raise ValidationError('此優惠券不存在')
    elif Information.objects(user_id=current_user.id, coupon__contain=coupon).first() != None:
        raise ValidationError('此優惠券已兌換')

class CouponForm(FlaskForm):
    coupon_id = HiddenField("",validators=[InputRequired(), validate_coupon])
    submit = SubmitField('提交')