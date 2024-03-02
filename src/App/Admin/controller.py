from flask import render_template
from App.Auth.auth_session import loggedInUser
def index():
    user_login = loggedInUser()
    return render_template('index.html', user_name = user_login.name, user=user_login)
