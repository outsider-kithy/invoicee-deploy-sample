from flask import redirect,render_template,request,url_for,flash,Blueprint
from werkzeug.security import generate_password_hash
from models import session,User

register = Blueprint(
    "register",
    __name__,
    template_folder="templates",
)

@register.route("/",methods=("GET","POST"))
def index():
    if request.method == "GET":
        return render_template("register/index.html")
    elif request.method == "POST":
        if not request.form.get('username'):
            error = "名前を入力してください"
            flash(error)
        elif not request.form.get("password"):
            error = "パスワードを入力してください"
            flash(error)
        elif not request.form.get("password_confirm"):
            error = "パスワードをもう一度入力してください"
            flash(error)
        else:
            username = request.form["username"]
            password = request.form["password"]
            password_confirm = request.form["password_confirm"]
            
            if password != password_confirm:
                error = "入力されたパスワードが一致しません"
                flash(error)
            else:
                error = None
                hashed = generate_password_hash(password)
                id = session.query(User).count()
                session.add(User(id = id + 1, username = username, password = hashed))
                session.commit()
                return redirect(url_for("login.index"))
            
        return render_template("register/index.html", error = error)

        