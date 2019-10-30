from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange
        
class PaymentForm(FlaskForm):
    payment = IntegerField("儲值金額",  validators=[InputRequired(), NumberRange(min=1, max=100000)])
    submit = SubmitField('確認')