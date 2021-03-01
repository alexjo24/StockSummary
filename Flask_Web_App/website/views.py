from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
#from .models import Note
from .models import HotStocks, DDStocks
from . import db
# import json

views = Blueprint('views', __name__)



@views.route('/', methods=['GET','POST'])
def home():

    return render_template("home.html", user=current_user)

@views.route('/hot', methods=['GET','POST'])
def hot():

    Hot_Stocks = HotStocks.query.all()


    return render_template("hot_section.html", Hot_Stocks=Hot_Stocks, user=current_user)


@views.route('/dd', methods=['GET','POST'])
def dd():

    DD_Stocks = DDStocks.query.all()


    return render_template("dd_section.html", DD_Stocks=DD_Stocks, user=current_user)


