from flask import Blueprint, render_template
from flask_login import login_required

from models import session, Job

top = Blueprint(
    "top",
    __name__,
    template_folder="templates",
)

@top.route("/")
@login_required
def index():
    jobs = session.query(Job).filter(Job.invoiced == 0).all()
    return render_template("top/index.html", jobs = jobs)