from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required

from models import session, Job, Work, Content, Tax

update = Blueprint(
    "update",
    __name__,
    template_folder="templates",
)

@update.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "GET":
        jobs = session.query(Job).filter(Job.invoiced == 0).all()
        works = session.query(Work).all()
        return render_template("update/index.html", jobs = jobs, works = works)
    
    elif request.method == "POST":
        error = None
        selected_job = request.form['job']
        work_type = request.form['work']
        content = request.form['content']

        if not selected_job:
            error = "ジョブが選択されていません"
            flash(error)
        elif not work_type:
            error = "作業の種類が選択されていません"
            flash(error)
        elif not content:
            error = "作業内容が入力されていません"
            flash(error)

        #選択したjobからjobIdを取得
        jobId = None
        job_id = session.query(Job).filter(Job.id == selected_job)
        for i in job_id:
            jobId = i.id
        session.close()

        #選択したwork_typeからwork_typeIdを取得
        workTypeId = None
        work_typeId = session.query(Work).filter(Work.work_type == work_type)
        for j in work_typeId:
            workTypeId = j.id
        session.close()

        #選択したwork_typeからtax_rateIdを取得
        # tax_rateId = None
        # tax_rateId = session.query(Work).filter(Work.work_type == work_type)
        # for k in tax_rateId:
        #     tax_rateId = k.id
        #     session.close()

        tax_rateId = None
        tax_rateId = session.query(Tax).join(Work).filter(Work.work_type == work_type)
        for k in tax_rateId:
            tax_rateId = k.id
            session.close()
        
            session.add(Content(job_id = jobId, work_id = workTypeId, work_content = content, tax_rate_id = tax_rateId))
            session.commit()

    return redirect(url_for("top.index"))