from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import session, Client, Tool, Work, Tax

admin = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
)

@admin.route("/", methods=("GET", "POST"))
@login_required
def index():
    #GETメソッドでアクセスしてきたら、index.htmlを表示
    if request.method == "GET":
        taxes = session.query(Tax).all()
        return render_template("admin/index.html", taxes = taxes)
    
    #POSTメソッドでデータが送られてきたら、それぞれClient、Toolテーブルにデータを登録
    elif request.method == "POST":
        client = request.form.get("client")
        tool = request.form.get("tool")
        tool_price = request.form.get("tool_price")
        tool_tax = request.form.get("tool_tax")
        work = request.form.get("work")
        work_price = request.form.get("work_price")
        work_tax = request.form.get("work_tax")
        error = None

        #clientに値が入っていれば
        if client:
            #現在のClientテーブルの件数+1した値を新しいデータのidに設定
            clientId = session.query(Client).count()
            session.add(Client(id = clientId + 1, client_name = client))

        #toolに値が入っていれば
        elif (tool is not None) & (tool_price is not None) & (tool_tax is not None):
            #現在のToolテーブルの件数に+1した値を新しいデータのidに設定
            toolId = session.query(Tool).count()
            #税率を選択
            taxId = session.query(Tax).filter(Tax.rate == tool_tax).all()
            tax_rate_id = None
            for i in taxId:
                tax_rate_id = i.id
            session.add(Tool(id = toolId + 1, tool_type = tool, price = tool_price, tax_rate_id = tax_rate_id))

        #workに値が入っていれば
        elif (work is not None) & (work_price is not None) & (work_tax is not None):
            workId = session.query(Work).count()
            taxId = session.query(Tax).filter(Tax.rate == work_tax).all()
            tax_rate_id = None
            for j in taxId:
                tax_rate_id = j.id
            session.add(Work(id = workId + 1, work_type = work, price = work_price, tax_rate_id = tax_rate_id))
        
        else:
            error = "何も入力されていません"
            flash(error)
            return render_template("admin/index.html", error = error)
        
        session.commit()

        return redirect(url_for("top.index"))