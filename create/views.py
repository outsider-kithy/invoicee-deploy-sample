from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required

from models import session, Job, Client, Tool, Tax

create = Blueprint(
    "create",
    __name__,
    template_folder="templates",
)

@create.route("/", methods=("GET","POST"))
@login_required
def index():
    #GETメソッドで/createにアクセスがあった場合は、
    #testデータベースから各項目一覧を選択肢としてform内に表示
    if request.method == "GET":
        tools = session.query(Tool).all()
        clients = session.query(Client).all()
        return render_template("create/index.html", tools = tools, clients = clients)
    
    #/createからPOSTメソッドで送られてきたデータを
    #testデータベースのJobテーブルに追加する
    elif request.method == "POST":
        title = request.form['title']
        tool = request.form['tool']
        client = request.form['client']
        error = None

        if not title:
            error = 'タイトルが入力されていません'
        if not tool:
            error = 'ツール名が選択されていません'
        if not client:
            error = 'クライアント名が選択されていません'
        if error is not None:
            flash(error)
        else:
            toolId = None
            clientId = None
            price = 0

            #POSTされたtoolの値に対応するtool_idを取得
            t = session.query(Tool).filter(Tool.tool_type == tool)
            for i in t:
                toolId = i.id

                #toolIdから価格を判定
                p = 0
                p = session.query(Tool).filter(Tool.id == toolId)
                for j in p:
                    price = j.price

            #POSTされたclientの値に対応するclient_idを取得
            c = session.query(Client).filter(Client.client_name == client)
            for l in c:
                clientId = l.id

                #testデータベースのJobテーブルに、新たなジョブを追加
                session.add(Job(
                    title = title,
                    tool_type_id = toolId,
                    client_id = clientId,
                    price = price,
                    invoiced = 0
                    ))
                session.commit()

            return redirect(url_for('top.index'))