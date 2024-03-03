from flask import render_template
from App.Auth.auth_session import loggedInUser
import App.Models.Category as CategoryInstance


def index():
    categories = CategoryInstance.ActiveQuery().all()
    return render_template('index.html', categories=categories)
