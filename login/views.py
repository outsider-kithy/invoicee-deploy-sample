from flask import Flask,redirect,render_template,request,url_for,flash,Blueprint
from flask_login import login_user
from werkzeug.security import check_password_hash
from models import session,User

login = Blueprint(
    "login",
    __name__,
    template_folder="templates",
)

@login.route("/",methods=("GET","POST"))
def index():
    if request.method == "GET":
        return render_template("login/index.html")
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error="名前を入力してください"
            flash(error)
        elif not password:
            error="パスワードを入力してください"
            flash(error)
        else:
            users = session.query(User).filter(User.username == username).all()
            for user in users:
                if not check_password_hash(user.password,password):
                    error="パスワードが違います"
                    flash(error)
                else:
                    login_user(user)
                    return redirect(url_for("top.index"))

    return render_template("login/index.html",error = error)