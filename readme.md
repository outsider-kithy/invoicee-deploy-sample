# PythonフレームワークFlaskアプリケーションをデプロイしよう サンプルコード

このリポジトリは、書籍「PythonフレームワークFlaskアプリケーションをデプロイしよう」のサンプルコードです。
※姉妹編「PythonフレームワークFlaskで請求書発行アプリを作ろう」の最終章`chap06`と同じ内容です。

## サンプルコードの環境構築
※このアプリケーションを動かすにはPostgreSQLのがインストールが必要です。

### Macの場合
ターミナルで以下を実行
```shell
#仮想環境「.venv」を作成
$ python3 -m venv .venv
#仮想環境をアクティベート
$ source .venv/bin/activate
#Flaskをインストール
(.venv) $ pip install flask
#dotenvをインストール
(.venv) $ pip install python-dotenv
#PostgreSQL関連のライブラリをインストール
(.venv) $ pip install sqlalchemy
(.venv) $ pip install flask_login
(.venv) $ pip install psycopg2
#openpyxlをインストール
(.venv) $ pip install openpyxl
#Flaskを起動
(.venv) $ flask run
```

### Windowsの場合
PowerShellで以下を実行
```shell
#仮想環境「.venv」を作成
python -m venv .venv
#仮想環境をアクティベート
.venv\Scripts\Activate.ps1
#Flaskをインストール
(.venv)　(略) pip install flask
#dotenvをインストール
(.venv)　(略) pip install python-dotenv
#PostgreSQL関連のライブラリをインストール
(.venv) (略) pip install sqlalchemy
(.venv) (略) pip install flask_login
(.venv) (略) pip install psycopg2
#openpyxlをインストール
(.venv) (略) pip install openpyxl
#Flaskを起動
(.venv)　(略) flask run
```


