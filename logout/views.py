from flask import Flask,redirect,Blueprint
from flask_login import login_required,logout_user

logout = Blueprint(
    "logout",
    __name__,
    template_folder="templates",
)

@logout.route("/")
@login_required
def index():
    logout_user()
    return redirect('/login')