from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user

import uuid, json, requests, shelve

from app import app
from app.models.payment import Payment
from app.forms.user.account.payment import PaymentForm

class PaymentView(MethodView):
    def get(self):
        form = PaymentForm(payment=100)
        return render_template('user/account/payment.html', form=form, hicoin=current_user.hicoin)
    
    def post(self):
        form = PaymentForm()

        if form.validate_on_submit():
            headers = {"X-LINE-ChannelId": app.config['CHANNEL_ID'],
                       "X-LINE-ChannelSecret": app.config['CHANNEL_SECRET'],
                       "Content-Type": "application/json; charset=UTF-8"}
            data = {"amount": form.payment.data,
                    "productName": "Hi幣",
                    "confirmUrl": app.config['APP_URL'] + url_for('payment_confirm'),
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

class PaymentConfirmView(MethodView):
    def get(self):
        payment = Payment.objects(payer_id=current_user.id, transaction_id=request.args.get('transactionId')).first()
        headers = {"X-LINE-ChannelId": app.config['CHANNEL_ID'],
                   "X-LINE-ChannelSecret": app.config['CHANNEL_SECRET'],
                   "Content-Type": "application/json; charset=UTF-8"}
        data = {"amount": payment.amount,
                "currency": payment.currency}
        response = requests.post(app.config['CHANNEL_CONFIRM_URL'].format(payment.transaction_id), headers=headers, data=json.dumps(data).encode('utf-8'))

        if int(json.loads(response.text)['returnCode']) == 0:
            payment.confirm = True
            payment.save()

            current_user.hicoin += payment.amount
            current_user.save()
        return redirect(url_for('payment'))