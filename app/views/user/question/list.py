from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.question import Question


class QuestionListView(MethodView):
    def get(self):
        questions = Question.objects(user_id=current_user.id)

        return render_template('user/question/list.html', questions=questions)
    def post(self):
    	pass