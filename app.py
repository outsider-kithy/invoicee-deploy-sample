import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import session
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager,login_manager

from models import session, User

#Macの場合はこちら
DATABASE_URL = 'postgresql://localhost/invoicee'
#Windowsの場合はこちら
#DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/invoicee'
engine = create_engine(DATABASE_URL,isolation_level='AUTOCOMMIT')
Base = declarative_base()
db_uri = os.environ.get(DATABASE_URL)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='secret_key'
    app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL

    login_manager.init_app(app)

    #register
    from register import views as register_views
    app.register_blueprint(register_views.register, url_prefix="/register")

    #login
    from login import views as login_views
    app.register_blueprint(login_views.login, url_prefix="/login")

    #top
    from top import views as top_views
    app.register_blueprint(top_views.top, url_prefix="/top")

    #create
    from create import views as create_views
    app.register_blueprint(create_views.create, url_prefix="/create")

    #update
    from update import views as update_views
    app.register_blueprint(update_views.update, url_prefix="/update")

    #invoice
    from invoice import views as invoice_views
    app.register_blueprint(invoice_views.invoice, url_prefix="/invoice")

    #admin
    from admin import views as admin_views
    app.register_blueprint(admin_views.admin, url_prefix="/admin")

    #logout
    from logout import views as logout_views
    app.register_blueprint(logout_views.logout, url_prefix="/logout")

    return app