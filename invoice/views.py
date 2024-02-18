from flask import Blueprint, render_template, request
from flask_login import login_required

from models import session, Job, Client, Content, Tax

#ヘルパー関数の読み込み
from helper import writeExcel

invoice = Blueprint(
    "invoice",
    __name__,
    template_folder="templates",
)

@invoice.route("/", methods=("GET", "POST"))
@login_required
def index():
    #GETメソッドでアクセスしてきた場合は、未請求のjob一覧をhtmlに表示
    if request.method == "GET":
        jobs = session.query(Job).filter(Job.invoiced == 0).all()
        return render_template("invoice/index.html", jobs = jobs)
    
    #POSTメソッドでデータが送られてきた場合は、請求書をExcel形式でエクスポートする
    elif request.method == "POST":
        #POSTされたjobデータを受け取る
        invoiceJobId = request.form['job']
        #POSTされてきたjobのidをキーに該当するデータを検索
        exportJob = session.query(Job).filter(Job.id == invoiceJobId).all()

        exportJobList = []

        for i in exportJob:
            #作業内容とその価格を検索して加算していく
            exportContents = None
            exportContentsPrice = None
            exportContentsCreated = None
            exportContentTaxRate = None
            contents = session.query(Content).join(Tax).filter(Content.job_id == invoiceJobId)

            #contentsを順番にexportJobListに追加していく
            for j in contents:
                #作業内容
                exportContents = j.work_content
                #価格
                exportContentsPrice = j.work.price
                #作業日
                exportContentsCreated = j.created
                #税率
                exportContentTaxRate = j.tax_rate.rate

                exportJobList.append([exportContents, exportContentsPrice, exportContentsCreated, exportContentTaxRate])

            #出力したjobを請求済みにする
            i.invoiced = 1
            session.commit()

            #請求書の宛先を検索・入力
            exportClientName = None
            client = session.query(Job).filter(Job.id == invoiceJobId).all()
            for c in client:
                clientId = c.client_id
                clientName = session.query(Client).filter(Client.id == clientId).all()
                for n in clientName:
                    exportClientName = n.client_name

                #ヘルパー関数のwriteExcelを使って、請求書を出力する
                exportFile = writeExcel(exportJobList, exportClientName)
                session.close()

                #exportJobListを空にする
                exportJobList = []
                return exportFile
