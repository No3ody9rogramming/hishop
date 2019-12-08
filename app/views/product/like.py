from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import SubmitField

from app.models.product import Product
from app.models.information import Information

class ProductLikeView(MethodView):
    def post(self, product_id):
        form = LikeForm()
        information = Information.objects(user_id=current_user.id).first()
        product = Product.objects(id=product_id).first()

        if form.validate_on_submit():
            if form.like.data == True:
                if product in information.like:
                    information.like.remove(product)
                    like = "far fa-heart"
                else:
                    information.like.append(product)
                    like = "fas fa-heart"
                information.save()

                return like
        return "error"

class LikeForm(FlaskForm):
    like = SubmitField('喜歡')