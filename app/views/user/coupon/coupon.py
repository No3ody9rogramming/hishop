from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from app.models.information import Information
from app.models.coupon import Coupon

import datetime

class CouponView(MethodView):
    def get(self):
        return render_template('user/coupon/coupon.html')
    def post(self):
        form = CouponForm()
        information = Information.objects(user_id=current_user.id).first()
        if form.validate_on_submit():
            coupon = Coupon.objects(id=form.couponID.data).first()
            information.coupon.append(coupon)
            information.save()
        return render_template('user/coupon/coupon.html')

def validate_coupon(form, couponID):
    coupon = Coupon.objects(id=couponID.data).first()
    informations = Information.objects().all()
    if coupon == None:
        raise ValidationError('此優惠券不存在')
    #testing reference: https://stackoverflow.com/questions/29222426/comparing-dates-in-flask-sqlalchemy
    #if want to find between the begin and end https://stackoverflow.com/questions/55148532/mongoengine-query-with-date-range
    elif coupon.due_time > datetime.datetime.utcnow():
        raise ValidationError('此優惠券已過期')
    else:
        for information in informations:
            if coupon in information.coupon:
                raise ValidationError('此優惠券已使用')
    


class CouponForm(FlaskForm):
    couponID = StringField("序號")
    submit = SubmitField('提交')