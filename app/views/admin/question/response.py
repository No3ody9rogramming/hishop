from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.question import Question

import datetime

QUESTION_STATUS = {"NO_ANSWER": "0", "ANSWER" : "1", "ALL": "2"}
class ResponseView(MethodView):
    def get(self, question_id):
        form = ResponseForm()

        question = Question.objects(id=question_id).first()

        return render_template('admin/question/response.html', form=form, question=question)
    
    def post(self, question_id):
        form = ResponseForm()
        if form.validate_on_submit():
            question = Question.objects(id=question_id).first()

            if question.response == None:
                question.response = form.response.data
                question.response_time = datetime.datetime.utcnow()
                question.save()

            return redirect(url_for('admin.response_list', status=QUESTION_STATUS["ANSWER"]))
        return render_template('admin/question/response.html', form=form)
        
class ResponseForm(FlaskForm):
    response = TextAreaField("問題回覆", render_kw={'rows': 7}, validators=[InputRequired(), Length(max=4000)])
    submit = SubmitField('提交')