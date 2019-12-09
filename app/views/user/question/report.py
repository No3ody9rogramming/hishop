from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.question import Question

class ReportView(MethodView):
    def get(self):
        form = ReportForm()

        return render_template('user/question/report.html', form=form)
    
    def post(self):
        form = ReportForm()
        if form.validate_on_submit():
            question = Question(user_id=current_user.id,
                                title=form.title.data,
                                detail=form.detail.data)
            question.save()
            return redirect(url_for('user.report'))
        return render_template('user/question/report.html', form=form)
        
class ReportForm(FlaskForm):
    title = StringField("問題主旨", validators=[InputRequired(), Length(max=20)])
    detail = TextAreaField("問題描述", render_kw={'rows': 7}, validators=[InputRequired(), Length(max=40)])
    submit = SubmitField('提交')