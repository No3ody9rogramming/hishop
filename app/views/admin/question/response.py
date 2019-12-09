from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.question import Question

class ResponseView(MethodView):
    def get(self):
        form = ResponseForm()

        return render_template('admin/question/response.html', form=form)
    
    def post(self):
        form = ResponseForm()
        if form.validate_on_submit():
            print()
            return redirect(url_for('response'))
        return render_template('admin/question/response.html', form=form)
        
class ResponseForm(FlaskForm):
    response = TextAreaField("回覆", render_kw={'rows': 7}, validators=[InputRequired(), Length(max=40000)])
    submit = SubmitField('提交')