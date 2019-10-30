from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField

from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError
        
class PublishForm(FlaskForm):
    name = StringField("商品名稱", validators=[InputRequired(), Length(max=50)])
    detail = CKEditorField("商品詳情")
    submit = SubmitField('上架')