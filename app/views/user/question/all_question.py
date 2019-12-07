from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.question import Question


class All_questionView(MethodView):
    def get(self):
        questions = Question.objects()

        return render_template('user/question/all_question.html', questions=questions)
    def post(self):
    	pass