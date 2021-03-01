import praw
from praw.models import MoreComments
import pandas as pd
from datetime import datetime
import calendar
import time
import sqlite3


def GetTickerSymbols():
    global nasdaq_df,nyse_df,amex_df
    print("Reading in Ticker Symbols")
    #CSV of stocksymbols located in the directory of the script.

    fields = ['Symbol','Name']
    #NASDAQ
    nasdaq_df = pd.read_csv('nasdaq_screener_1613033542544_NASDAQ.csv',usecols = fields)
    #NYSE
    nyse_df = pd.read_csv('nasdaq_screener_1613033608613_NYSE.csv', usecols = fields)
    #AMEX
    amex_df = pd.read_csv('nasdaq_screener_1613033634897_AMEX.csv', usecols = fields)


#Purpose of this method is to clean the submission/comment data.
#Remove empty elements, ','-sign, '.'-signs.
#
def cleanData(post):
    # Split text of post into a list & remove "," and "." signs from the list.
    postText = [y.strip(',.') for y in post.split(' ')]

    # Remove empty elements from list.
    postText = list(filter(None,postText))

    #Removing typically used words to not identify them as stock symbols.
    rm_list = ['One','one','Green','NOW','NEW','Just','At','Red', 'GO', 'ROCKET']

    for rm_el in rm_list:
        if rm_el in postText:
            postText.remove(rm_el)


    return postText

#Frequency of scraping
def Timer():
    pass

#####Implemented different rules to avoid unneccessary searches and for identifying symbols accurately
#
# The post text is split into a list where each word is an element.
# Continue with each rule if no match is found in the post text.
# E.g. if rule 1 couldnt find a match then continue to rule 2 and so on.
#
# Rules:
#
# 1. Search for full company name in a post. Only use first part of the name.
#    Remove 'The' when comparing stock name to post text.
#
# 2. Search for words that start with a $-sign.
#
# 3. Get the length of the word of an element and search for symbols with corresponding length from the NYSE,NASDAQ,AMEX csv files.
#    If a symbol is not identified from the post text, continue and search for length of the word - 1, then len(word) - 2, etc.
#    Stop when len(word) - counter  = 1, i.e. ignore 1 letter size words.
#
#    This rule can identify symbols when people write the following: TSLA???
#
# 4. Search for stock symbols with (" "+symbol+" ") .
#    Limit only to 3 symbol sized stocks and only check for capital letter words.
#
#    The issue with this method is that symbol stocks will be identified "wrongly". But if there is a stock trending it
#    will be mentioned more than the wrongly identified stocks. I.e. the faulty data being picked up by the "wrongly"
#    identified stocks will (most likely) be outnumbered by a great percentage.

def FindTickerSymbolsMatches(post):

    postText = cleanData(post)


    #Iterate through all stocksymbol.csv files.

    df_list = [nyse_df, nasdaq_df, amex_df]
    
    for df in df_list:

        for id, row in df.iterrows():
            #Rule 1.
            nameOfStock = str(row.Name.split(' ')[0])

            if nameOfStock == 'The':
                nameOfStock = str(row.Name.split(' ')[1])

            if nameOfStock in postText:
                # print('RULE 1: ', nameOfStock,' : ',postText)
                return str(row.Symbol),str(row.Name)

            #Rule 2.
            for el in postText:
                #if el != '':
                if '$' == el[0]:

                    symbolOfStock = el[1:]

                    if symbolOfStock == row.Symbol:
                        # print('RULE 2: ', nameOfStock,' : ',postText)
                        return str(row.Symbol),str(row.Name)

            #Rule 4.
            for el2 in postText:
                if el2.isupper() and el2 == row.Symbol and len(row.Symbol) > 2:
                    # print('RULE 4: ', nameOfStock, ' : ', postText)
                    return str(row.Symbol),str(row.Name)



def WebScrapeReddit():
    reddit = praw.Reddit(client_id = 'insert',
                         client_secret = 'insert',
                         username = 'insert',
                         password = 'insert',
                         user_agent = 'something')


    #Subreddit to webscrape
    subreddit = reddit.subreddit('wallstreetbets')

    ##################### Front page, Hot section
    print()
    print(50 * '#')
    print("Front page Hot Section")
    print()
    hot_section = subreddit.hot(limit=40)
    hotlist = searchInSub(hot_section)
    saveToDatabase(hotlist,"hot") #Save data to database, keyword used to store data in the correct database.

    ##################### Daily Discussion Thread, comments. At 12 daily local time a new daily discussion submission is posted.
    print()
    print(50 * '#')
    print("Daily Discussion Thread, comment section")
    print()

    dailyDiscussion = subreddit.search('flair_name:"Daily Discussion"', sort='new', limit = 1)
    ddlist = searchInComments(dailyDiscussion)
    saveToDatabase(ddlist,"dd") #Save data to database, keyword used to store data in the correct database.


    # ##################### Daily DD section, hot
    # print(50 * '#')
    # print("Daily DD Section")
    # daily_dd = subreddit.search('flair:DD', sort='hot',time_filter = 'day')
    #
    # searchInSub(daily_dd)




#Search for stock in submission text
def searchInComments(section):

    stockList = []

    cc_tmp = 0
    cc = 0

    t0 = time.time()

    for post in section:
        # if checkDate(post):
        #     continue

        print(post.title)

        # See https://praw.readthedocs.io/en/latest/tutorials/comments.html for more details.
        post.comments.replace_more(limit=1)
        for comment in post.comments.list():
            #print(comment.body)
            stock = FindTickerSymbolsMatches(comment.body)
            if stock != None:
                stockList.append(stock)

            cc += 1


        # post.comments.replace_more(limit=4)
        # for top_level_comment in post.comments:
        #     print(top_level_comment.body,' :::: ', top_level_comment.ups)
        #     cc+=1
    print(stockList)
    print(len(stockList))
    print()
    print(50 * '#')
    print('Amount of comments: ', str(cc))
    t1 = time.time()
    total = t1 - t0
    print('Total time: ', int(total), 'seconds')

    
    # Count amount of mentions for each stock and return in a list of lists.
    listSummary = countMentions(stockList)

    return listSummary



#Search for stock in comment section
def searchInSub(section):

    stockSubList = []

    for post in section:
        if not post.stickied:
            print()
            #print('Title: {}, Upvotes: {}, Comments: {}'.format(post.title, post.ups, post.num_comments))
            print(str(post.title))
            print(FindTickerSymbolsMatches(str(post.title)))
            stock = FindTickerSymbolsMatches(str(post.title))
            if stock != None:
                stockSubList.append(stock)

    # Count amount of mentions for each stock and return in a list of lists.
    listSummary = countMentions(stockSubList)

    return listSummary

#Count the amount of mentions of a stock and store mentions and respectively company in descending order.
def countMentions(listOfStocks):

    stockSummary = []

    #Obtain unique stock symbols.
    uniqueList = list(set(listOfStocks))
    print("Unique stock symbol list: ",listOfStocks)

    # Count how many times a unique stock symbol is found in the list of all the stock mentions.
    for uniqueSym in uniqueList:
        cc = 0
        for el in listOfStocks:
            if el[0] == uniqueSym[0]:
                cc += 1
        

        #Add mentions and stock information in a summary list.
        stockSummary.append([uniqueSym[0], uniqueSym[1], cc])

    #Sort list in descending order in regards to amount of mentions.
    stockSummary = sorted(stockSummary, key=lambda x: int(x[2]), reverse = True)

    print("Stocksummary sorted: ", stockSummary)

    return stockSummary



#Store summary of stock mentions, list of lists format, in database.db which is created through the flask web app.
def saveToDatabase(listSummary,keyword):

    #The list of list is transformed into a dataframe. Necessary step to save webscraped data onto the database.db.
    df_stockSummary = pd.DataFrame.from_records(listSummary,columns=['stock_symbol', 'stock_company', 'stock_mentions'])
    # df_stockSummary.insert(0, 'id', df_stockSummary.index+1)
    print(df_stockSummary)

    try:
        conn = sqlite3.connect('Flask_Web_App\website\database.db')  
        c = conn.cursor()
    except Exception as e:
        print(e)


    if keyword == 'hot':
        df_stockSummary.to_sql('hot_stocks', conn, if_exists='append', index = False)
    elif keyword == 'dd':
        df_stockSummary.to_sql('dd_stocks', conn, if_exists='append', index = False)
    





if __name__ == '__main__':
    GetTickerSymbols()
    WebScrapeReddit()


############################################
# def runDays():

#     weekno = datetime.datetime.today().weekday()

#     if weekno < 5:
#         print("Weekday")
#         print("RUNNING SCRIPT")
#     else:
#         print("Weekend")
#         print("Not Running Script!")



############################################


# def checkDate(post):
#     print(post.title)
#     #print(str(datetime.today()).split(" ")[0].split("-"))

#     year,month,day = str(datetime.today()).split(" ")[0].split("-")

#     month = calendar.month_abbr[int(month)]

#     print(year,month,day)

#     if year in post.title and month in post.title and day in post.title:
#         print("Date Correct")

#         return True
#     else:
#         print("Post does not match the correct Date")

#         return False


############################################

#Save stock summary to csv file
# def saveToCSV(a):
#     with open("data.csv", "wb") as f:
#         writer = csv.writer(f)
#         writer.writerows(a)

############################################

# # Rule 3.
# for el2 in postText:
#     len_word = len(el2)
#
#     # Ignore 1 and 2 length symboled stocks.
#     # Assuming that the user writing the post want to clarify and write the entire company name when a 1 or 2 length
#     # symbol stock is written for clarification/understanding. E.g. F, Ford Company. Rule 1 would catch that stock.
#     while len_word > 2:
#
#         for id, row in nyse_df.iterrows():
#
#             if len_word == len(row.Symbol):
#                 #print(' inside: ', el2[:len_word], ' ::::: ', row.Symbol)
#                 if el2[:len_word] == row.Symbol:
#                     return str(row.Symbol),str(row.Name)
#
#         len_word -= 1