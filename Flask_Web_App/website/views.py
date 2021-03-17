from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
#import json
from collections import defaultdict

views = Blueprint('views', __name__)



@views.route('/', methods=['GET','POST'])
def home():

    Hot_Stocks_5 = HotStocks.query.limit(5)

    DD_Stocks_5 = DDStocks.query.limit(5)

    return render_template("home.html", DD_Stocks_5=DD_Stocks_5,Hot_Stocks_5=Hot_Stocks_5, user=current_user)

@views.route('/hot', methods=['GET','POST'])
def hot():

    Hot_Stocks = HotStocks.query.all()


    return render_template("hot_section.html", Hot_Stocks=Hot_Stocks, user=current_user)


@views.route('/dd', methods=['GET','POST'])
def dd():

    DD_Stocks = DDStocks.query.limit(20)
    ls_vis_Stocks, ls_vis_values, date_list = dbToList()    #Exports the data from the database table data restructure it for visualization purposes.
                                                            #Three lists are output from the method:
                                                            # ls_vis_Stocks: the top ten stocks symbols. (String)
                                                            # ls_vis_value: the stock symbol respective stock mentions for the last week. (Int)
                                                            # date_list: respective dates in the order which matches the when a stock mention was webscraped. (String)
    return render_template("dd_section.html", DD_Stocks=DD_Stocks, user=current_user, ls_vis_Stocks=ls_vis_Stocks, ls_vis_values=ls_vis_values, date_list=date_list)

#Convert database table data to lists. This is to enable visualization with chart.js.
#This code was altered many times to be able to get the data to the .html page.
# Many quickfixes was used for fast debugging and trying to understand what works best with the chart.js implementation in the .html.
#In other words dbToList method code can be greatly refined.
def dbToList():

    #Load in reverse order to get the dates in ascending order in chart.js visualization
    dd0 = DDStocks.query.limit(10)
    dd1 = DDStocks1d.query.limit(10)
    dd2 = DDStocks2d.query.limit(10)
    dd3 = DDStocks3d.query.limit(10)
    dd4 = DDStocks4d.query.limit(10)
    dd5 = DDStocks5d.query.limit(10)
    dd6 = DDStocks6d.query.limit(10)
    dd7 = DDStocks7d.query.limit(10)

    dd_list = [dd0, dd1, dd2, dd3, dd4, dd5, dd6, dd7]
    dd_list.reverse()

    stockSymbol_list, value_list = getStockSymbols(dd_list)  #Obtain a list of all the stocks that have been in the top ten a week back.
    dict_mentions = dict(zip(stockSymbol_list,value_list)) #Creates a dictionary from two lists.

    date_list = []

    for c,dd_idx in enumerate(dd_list):
        for cc,item in enumerate(dd_idx):
            
            if cc == 0:
                date_list.append(item.stock_date)

            for key,value in dict_mentions.items():

                if item.stock_symbol == key:
                    dict_mentions[key].append(item.stock_mentions)

        #Add a zero to those keys who did not get a value assigned.
        for key, value in dict_mentions.items():
            if len(dict_mentions[key]) == c:
                dict_mentions[key].append(0)  
                

    #Converting keys and values to seperate lists for chart.js implementation in the .html file.
    ls_vis_Stocks = list(dict_mentions.keys())
    ls_vis_values = list(dict_mentions.values())


    return ls_vis_Stocks,ls_vis_values, date_list

#Get a list of all stock symbols that has been on the top ten latest week.
def getStockSymbols(dd_list):
    
    stockSymbol_list = []
    value_list = [] #used to create a dictionary with seperate lists to append data.

    for dd_idx in dd_list:
        for item in dd_idx:
            if item.stock_symbol not in stockSymbol_list:
                stockSymbol_list.append(item.stock_symbol)
                value_list.append([])

    return stockSymbol_list, value_list

