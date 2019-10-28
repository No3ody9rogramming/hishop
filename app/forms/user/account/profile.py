from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError
        
class ProfileForm(FlaskForm):
    name = StringField("名稱", validators=[InputRequired(), Length(max=50)])
    phone = StringField("電話號碼", validators=[InputRequired(), Length(max=15)])
    submit = SubmitField('修改')