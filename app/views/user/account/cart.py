from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

import uuid, json, requests, shelve

from app import app
from app.models.payment import Payment
from app.models.information import Information

class CartView(MethodView):
    def get(self):
        form = CartForm()
        products = Information.objects(user_id=current_user.id).first().cart
        return render_template('user/account/cart.html', form=form, hicoin=current_user.hicoin, products = products)
    
    def post(self):
        form = CartForm()

        if form.validate_on_submit():
            print(url_for('static', filename='hicoin.png', _external=True))
            headers = {"X-LINE-ChannelId": app.config['CHANNEL_ID'],
                       "X-LINE-ChannelSecret": app.config['CHANNEL_SECRET'],
                       "Content-Type": "application/json; charset=UTF-8"}
            data = {"amount": form.payment.data,
                    "productName": "Hi幣",
                    "productImageUrl": url_for('static', filename='hicoin.png', _external=True),
                    "confirmUrl": url_for('payment_confirm', _external=True),
                    "orderId": uuid.uuid4().hex,
                    "currency": "TWD"}
            response = requests.post(app.config['CHANNEL_URL'], headers=headers, data=json.dumps(data).encode('utf-8'))
            
            if int(json.loads(response.text)['returnCode']) == 0:
                payment = Payment(payer_id=current_user.id,
                                  transaction_id = json.loads(response.text)['info']['transactionId'],
                                  amount=form.payment.data,
                                  currency="TWD",
                                  confirm=False).save()
                return redirect(json.loads(response.text)['info']['paymentUrl']['web'])

        return redirect(url_for('payment'))


class CartForm(FlaskForm):
    submit = SubmitField('結帳GO')