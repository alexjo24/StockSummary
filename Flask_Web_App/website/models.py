from . import db  
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  #db.String(150) sets the maximum amount of emails to 150 ,unique=True, users cant have the same email.
    password = db.Column(db.String(150), nullable=False)
    userName = db.Column(db.String(150), unique=True, nullable=False)
    phonenumber = db.Column(db.String(150),unique=True,nullable=False) # Phonenumber is unique per user. Using string to be able to use landcode "+"-sign.


####################### Hot Stocks TABLE ##########################
###################################################################

class HotStocks(db.Model):
    __tablename__ = 'hot_stocks'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)


####################### DD STOCKS TABLES ##########################
###################################################################
# Store data 7 days back in seperate tables

class DDStocks(db.Model):
    __tablename__ = 'dd_stocks'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)


class DDStocks1d(db.Model):
    __tablename__ = 'dd_stocks1d'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)

class DDStocks2d(db.Model):
    __tablename__ = 'dd_stocks2d'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)

class DDStocks3d(db.Model):
    __tablename__ = 'dd_stocks3d'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)

class DDStocks4d(db.Model):
    __tablename__ = 'dd_stocks4d'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)

class DDStocks5d(db.Model):
    __tablename__ = 'dd_stocks5d'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)

class DDStocks6d(db.Model):
    __tablename__ = 'dd_stocks6d'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)

class DDStocks7d(db.Model):
    __tablename__ = 'dd_stocks7d'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    stock_company = db.Column(db.String(150), nullable=False)
    stock_mentions = db.Column(db.Integer, nullable=False)


