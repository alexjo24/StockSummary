import sys, os
from twilio.rest import Client
import time
import sqlite3
import pathlib
import schedule

#Twilio only allows to send messages to phonenumbers connected to the twilio sandbox. For this solution to work a paid subscription or similar is needed for being able to send messages to different whatsapp phonenumbers...



#Send a whatsapp message each day at 11:00
def sendTime():
	schedule.every().day.at("11:00").do(sendWhatsApp)

	while True:
		schedule.run_pending()
		time.sleep(60) # wait one minute


def sendWhatsApp():


	while True:
		currentdir = str(pathlib.Path(__file__).parent.absolute()) + "\\"

		try:
			conn = sqlite3.connect(currentdir+'database.db')  
			c = conn.cursor()

		
			c.execute("SELECT userName,phonenumber FROM user")
			rowsUser = c.fetchall()
			
			

			c.execute("SELECT id,stock_symbol,stock_mentions FROM dd_stocks LIMIT 5")
			rowsStock = c.fetchall()

			
			stockText = 'Id, Stock, #Mentions \n\n'
			for row in rowsStock:
				stockText = stockText + str(row[0])+', '+row[1]+', '+str(row[2]) + '\n'
				
			
			for user in rowsUser:
				
				text = "Hello "+user[0]+'\n'+'Here is the top mentioned stocks of the day: \n\n' + stockText + '\nHave an awesome day!\n'
				phonenumber = user[1]

				print('¤'*20)
				print(phonenumber)
				print(text)
				
				message(phonenumber,text)

		except sqlite3.Error as error:
			print(error)
		finally:
			if conn:
				conn.close()



def message(phonenumber,text):

	account_sid = 'INSERT'
	auth_token = 'INSERT'
	client = Client(account_sid, auth_token)
	message_send = text
	message = client.messages.create(
		from_='whatsapp:+14155238886',
		body=message_send,
		to='whatsapp:'+phonenumber
	)


