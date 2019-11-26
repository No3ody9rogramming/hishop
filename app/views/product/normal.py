from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

import datetime

from app.models.product import Product
from app.models.information import Information, History

class ShowNormalView(MethodView):
    def get(self, product_id):
        form = ReportForm()
        product = Product.objects(id=product_id).first()
        
        if product == None:
            abort(404)
        if current_user.is_active:
            #update history
            information = Information.objects(user_id=current_user.id).first()
            update = False
            for history in information.history:
                if history.product_id.id == product.id:
                    history.create_time = datetime.datetime.utcnow()
                    update = True
                    break
            if update == False:
                information.history.append(History(product_id=product.id))
            information.save()

            #update view times
            product.view += 1
            product.save()
        return render_template('product/normal.html', form=form, product=product, product_json=product.to_json())


    
    def post(self, product_id):
        form = ReportForm()
        if form.validate_on_submit():
            question = Question(user_id=current_user.id,
                                title=form.title.data,
                                detail=form.detail.data)
            question.save()
            return redirect(url_for('report'))
        return render_template('user/question/report.html', form=form)
        
class ReportForm(FlaskForm):
    like = SubmitField('喜歡')
    cart = SubmitField('加入購物車')