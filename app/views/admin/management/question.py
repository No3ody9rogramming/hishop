from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.question import Question

QUESTION_STATUS = {"NO_ANSWER": "0", "ANSWER" : "1", "ALL": "2"}
class AdminQuestionView(MethodView):
    def get(self):
        questions = Question.objects()

        status = request.args.get('status')
        if status == QUESTION_STATUS['NO_ANSWER']:
            questions = Question.objects(response=None)
        elif status == QUESTION_STATUS['ANSWER']:
            questions = Question.objects(response__ne=None)
        else:
            status = QUESTION_STATUS['ALL']
            questions = Question.objects()

        questions = sorted(questions, key=lambda k: k.create_time, reverse=False)

        return render_template('admin/management/question.html', questions=questions, QUESTION_STATUS=QUESTION_STATUS, status=status)