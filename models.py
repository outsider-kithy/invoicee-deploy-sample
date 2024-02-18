import os
from sqlalchemy import Column,Integer,String,Numeric,ForeignKey,create_engine
from sqlalchemy.orm import relationship, sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.sql.sqltypes import Date
from flask_login import UserMixin

#データベース関係の設定
#Macの場合はこちら
DATABASE_URL = 'postgresql://localhost/invoicee'
#Windowsの場合はこちら
#DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/invoicee'
engine = create_engine(DATABASE_URL,isolation_level='AUTOCOMMIT')
Base = declarative_base()
db_uri = os.environ.get(DATABASE_URL)

#セッションの設定
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

#ユーザーテーブル
class User(UserMixin,Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String, unique = True)
    password = Column(String)

#クライアントテーブル
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key = True, autoincrement = True)
    client_name = Column(String)

    job = relationship("Job", back_populates = "client")

#税率テーブル
class Tax(Base):
    __tablename__ = 'tax'
    id = Column(Integer, primary_key = True, autoincrement = True)
    rate = Column(Numeric(precision=4, scale=2))

#ツールテーブル
class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key = True ,autoincrement = True)
    tool_type = Column(String)
    price = Column(Integer)
    tax_rate_id = Column(Integer, ForeignKey("tax.id"))
    
    job = relationship("Job", back_populates = "tool_type")
    tax_rate = relationship("Tax")

#作業テーブル
class Work(Base):
    __tablename__ = "works"
    id = Column(Integer, primary_key = True, autoincrement = True)
    work_type = Column(String)
    price = Column(Integer)
    tax_rate_id = Column(Integer, ForeignKey("tax.id"))

    tax_rate = relationship("Tax")

#ジョブテーブル
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String)
    created = Column(Date, index=True, default = datetime.date.today())
    tool_type_id = Column(Integer, ForeignKey("tools.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    price = Column(Integer)
    invoiced = Column(Integer)

    tool_type = relationship("Tool")
    client = relationship("Client")
    content = relationship("Content")

#作業内容テーブル
class Content(Base):
    __tablename__ = "contents"
    id = Column(Integer, primary_key = True, autoincrement = True)
    created = Column(Date, index = True, default = datetime.date.today())
    job_id = Column(Integer, ForeignKey("jobs.id"))
    work_id = Column(Integer, ForeignKey("works.id"))
    work_content = Column(String)
    tax_rate_id = Column(Integer, ForeignKey("tax.id"))

    job = relationship("Job", back_populates="content")
    work = relationship("Work")
    tax_rate = relationship("Tax")
