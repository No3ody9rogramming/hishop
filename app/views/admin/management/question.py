from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, TextAreaField, HiddenField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.question import Question

import datetime

QUESTION_STATUS = {"NO_ANSWER": "0", "ANSWER" : "1", "ALL": "2"}
class AdminQuestionView(MethodView):
    def get(self):
        questions = Question.objects()
        form = ResponseForm()

        status = request.args.get('status')
        if status == QUESTION_STATUS['NO_ANSWER']:
            questions = Question.objects(response=None)
        elif status == QUESTION_STATUS['ANSWER']:
            questions = Question.objects(response__ne=None)
        else:
            status = QUESTION_STATUS['ALL']
            questions = Question.objects()

        questions = sorted(questions, key=lambda k: k.create_time, reverse=False)

        return render_template('admin/management/question.html', questions=questions, QUESTION_STATUS=QUESTION_STATUS, status=status, form=form)

    def post(self):
        form = ResponseForm()

        if form.validate_on_submit():
            question = Question.objects(id=form.question_id.data).first()
            
            print(question.title)
            if question.response == None:
                question.response = form.response.data
                question.response_time = datetime.datetime.utcnow()
                question.save()

            return redirect(url_for('admin.question', status=QUESTION_STATUS["ANSWER"]))
            
        return render_template('admin/management/question.html', form=form)
        
class ResponseForm(FlaskForm):
    question_id = HiddenField("", validators=[InputRequired()])
    response = TextAreaField("問題回覆", render_kw={'rows': 7, 'cols':55}, validators=[InputRequired(), Length(max=4000)])
    submit = SubmitField('提交')