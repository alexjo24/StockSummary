from website import create_app
from threading import Thread, Event, Timer
from website.message import sendTime
import time
from multiprocessing import Process
import os
from datetime import datetime, timedelta

#For flask being able to run in a separate thread or with multiprocess, debug = False. It will not work with debug = True.
# Ref https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread#:~:text=Flask%20can%20run%20just%20fine,or%20disable%20the%20reloader%20(%20app.
# Another solution is to use ray. Using ray would have been the preferred solution but it is not supported in python 3.9 yet.

#Multiprocess solution (currently used.)
def runAppMulti():
    print("Running flask app")

    app = create_app()
    app.run(debug=False)  


def sendingMessageMulti():
    print("Sending messages")
    while True:
        time.sleep(2)
        sendTime()

#Thread solution (currently not used.)
#Reference: https://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
def runAppThread(run_event):
    print("Running flask app")
    while run_event.is_set():
        app = create_app()
        app.run(debug=False)  
        #app.run(debug=True)  #Only debug = True while work in progress´
        time.sleep(1)


def sendingMessageThread(run_event):
    print("Sending messages")
    while run_event.is_set():
        time.sleep(2)
        sendTime()



if __name__ == '__main__':

    ##############Multiprocess solution

    
    p1 = Process(target=sendingMessageMulti)
    p1.start()
    
    
    p2 = Process(target=runAppMulti)
    p2.start()
    

    ##############Thread solution

    # run_event = Event()
    # run_event.set()
    
    # t1 = Thread(target=runAppThread, args = (run_event,))

    # t2 = Thread(target=sendingMessageThread, args = (run_event,))

    # t1.start()
    # time.sleep(.5)
    # t2.start()
    # try:
    #     while 1:
    #         time.sleep(.1)
    # except KeyboardInterrupt:
    #     print("Attempting to close threads.")
    #     run_event.clear()
    #     t1.join()
    #     t2.join()
    #     print("threads successfully closed")