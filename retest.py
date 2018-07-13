import requests
import json
import indicators
from lxml.html import fromstring
#import requests
from itertools import cycle
import time
import sys
import test2
import db_market
import numpy
from datetime import datetime
from datetime import timedelta
import datetime
import queue

import threading
#z = datetime.datetime(2018,06,14)
ticker = 'gme'
db = db_market.market()
db.setTicker(ticker)


readable = time.ctime(1528934100)
startDate = 1527811200000
enddate = 1527811200000

#print(readable)

with open('authtoken','r') as f:
    toke = f.readline()

token = 'Bearer {}'.format(toke)
header = {'Authorization': token }

# print(url)
ind = True
up = False

start = '2018-06-01 00:00:00'
end = '2018-07-12 23:00:00'

tickerQueue = queue.Queue()
def queueTickers():

    with open('TICKERS','r') as f:
        ticks = f.readlines()
        q = queue.Queue()
        [q.put(ticker.strip()) for ticker in ticks]
        return q
#q = queue.Queue()
    #print(q.get())
def gethist(ticker):
    print(ticker)
num_api_threads = 2
def APIworker():
    while True:
        #print("Waiting for ticker")
        ticker = tickerQueue.get()
        if tickerQueue == None:
            tickerQueue.task_done()
            break
        gethist(ticker)
        tickerQueue.task_done()
for i in range(num_api_threads):
    t = threading.Thread(target = APIworker)
    t.start()

q = queueTickers()
# while not q.empty():
#     tickerQueue.put(q.get())

    # print(q.get())

# print(response.text)
# j = json.dumps(response.text)
# # print(response.text)
# #
# with open("test.txt",'w') as f:
#     json.dump(response.text,f,ensure_ascii=False)


def getHistorical(startDate,endDate,ticker):
    url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory?periodType=day&frequencyType=minute&frequency=15&endDate={}&startDate={}&needExtendedHoursData=false'.format(
        ticker,endDate, startDate)

    response = requests.get(url,headers = header)
    if response.status_code == 200:

        j = json.dumps(response.text)
        #print(j)
        with open("test.txt", 'w') as f:
           json.dump(response.text,f,ensure_ascii=False)

    else:
        print(response.status_code)
        print("failed")

    return response

def update(lastChecked,ct):
    #lastChecked = db.getLastUpdated(ticker)[0].strftime('%Y-%m-%d')
    today = datetime.datetime.now().strftime('%Y-%m-%d')


    if today > lastChecked:

        print("UPDATING")
        endDate = datetime.datetime.strptime(today,'%Y-%m-%d')
        startDate = datetime.datetime.strptime(lastChecked,'%Y-%m-%d')

        #update
        delta = endDate - startDate
        print(delta.days)
        startDate = startDate + timedelta(days=1)
        startDate = int(startDate.timestamp() * 1000)
        endDate     = int(datetime.datetime.now().timestamp() * 1000)
        print(startDate)
        print(endDate)

        response = getHistorical(startDate,endDate,ct)
        if response.status_code == 200:

            db.insertResults(response.text)



while not q.empty() and up:
    currentTicker = q.get()
    db.setTicker(currentTicker)

    exists = db.doesTableExist(currentTicker)
    if(exists):
        try:
            lastChecked = db.getLastUpdated(currentTicker)[0].strftime('%Y-%m-%d')
            update(lastChecked,currentTicker)
            print(lastChecked)
        except:
            print("error")
            response = getHistorical(startDate,enddate,currentTicker)
            if response.status_code == 200:
                db.insertResults(response.text)
            q.put(currentTicker)
    else:
        db.createTable(currentTicker)
        #add back to queue
        q.put(currentTicker)





# with open('test.txt','r') as f:
#     file = json.loads(f.read())



# while not q.empty():
#     currentTicker = q.get()
#     db.setTicker(currentTicker)
#
#     RelativeVolume = []
#     RelativeVolumeAvg = []
#     TrueRange = []
#
#     # print("Checking : {}".format(currentTicker))
#     x = list(db.getFromPeriod(currentTicker, start, end))
#     for index, row in enumerate(x[-60:]):
#         #print(row)
#         i = x.index(row)
#         #print(x.index(row))
#         rvtest(10, x, row)
def printRV(RV,period):

    print(RV[-period:])

#q = queueTickers()


# while not q.empty() and not ind:
#
#     currentTicker = q.get()
#     db.setTicker(currentTicker)
#
#     RelativeVolume      =[]
#     RelativeVolumeAvg   =[]
#     TrueRange           =[]
#
#     #print("Checking : {}".format(currentTicker))
#     x = list(db.getFromPeriod(currentTicker, start, end))
#     lessThanDate = datetime.datetime.strptime('2018-06-10','%Y-%m-%d')
#
#     for index, row in enumerate(x[-500:]):
#         #print(currentTicker)
#         if(row[6] >= lessThanDate):
#             rv = round(indicators.getRelativeVolume(10,x,row),2)
#             tr = indicators.addTrueRange(row)
#
#
#
#             TrueRange.append(tr)
#             RelativeVolume.append(rv)
#
#             rvAvg = indicators.getRelativeVolumeAverage(RelativeVolume, 10)
#             RelativeVolumeAvg.append(rvAvg)
#             #indicators.checkChurn(RelativeVolume,TrueRange,row,rvAvg,currentTicker,rv)
#             indicators.jeremyCator(RelativeVolume,rv,currentTicker,row)

                #printRV(RelativeVolume,10)

        # if RVavg > 300:
        #     print("Avg RV:  {}\n"
        #           "At:      {}".format(RVavg,row[6]))
    # for index, row in enumerate(x[-10:]):
    #     #print(row[6])
    #     p =x.index(row)
    #     #print(p)
    #     print("Starting Period  :{}\n"
    #           "Volume           :{}".format(row[6],row[5]))
    #     barDate = row[6]
    #     v = []
    #
    #     for i in range(1,11):
    #         row_at_multiplyer = x[(p - i*multiplyer)]
    #
    #         v.append(row_at_multiplyer[5])
    #         #print("Last Period:   {}".format(row_at_multiplyer[6]))
    #         #print(row_at_multiplyer)
    #
    #     rv = (row[5] / numpy.average(v)) * 100
    #     print(round(rv,2))
    #
    #     v = []


def parse(x,currentTicker):
    #currentTicker = q.get()
    #db.setTicker(currentTicker)

    RelativeVolume = []
    RelativeVolumeAvg = []
    TrueRange = []

    # print("Checking : {}".format(currentTicker))

    lessThanDate = str(datetime.datetime.strptime('2018-07-12', '%Y-%m-%d'))
    show = True
    for index, row in enumerate(x[-150:]):
        # print(currentTicker)
        d = datetime.datetime.strftime(row[6], '%Y-%m-%d 00:00:00')

        if (d == lessThanDate):
            rowIndex = x.index(row)
            rv = round(indicators.getRelativeVolume(10, x, row), 2)
            tr = indicators.addTrueRange(row)

            TrueRange.append(tr)
            RelativeVolume.append(rv)
            ATR = numpy.average(TrueRange[-10:])
            if( ATR> .20):

                #print(currentTicker)
                #print(ATR)
                rvAvg = indicators.getRelativeVolumeAverage(RelativeVolume, 10)
                RelativeVolumeAvg.append(rvAvg)
                #indicators.checkChurn(RelativeVolume,TrueRange,row,rvAvg,currentTicker,rv)
                indicators.jeremyCator(RelativeVolume, rv, currentTicker, row,TrueRange)
                #indicators.churning(rvAvg,x,TrueRange,currentTicker,row)
                #indicators.swinglow(x[(rowIndex-2):rowIndex+1],currentTicker)
num_indicator_thread = 2
indicator_queue = queue.Queue()
def indicator():
    while True:
        #print("Waiting parse for indicators")
        ob = indicator_queue.get()
        h = ob[0]
        ticker = ob[1]

        if h == None:
            indicator_queue.task_done()
            break
        parse(h,ticker)
        indicator_queue.task_done()

for i in range(num_indicator_thread):
    t = threading.Thread(target = indicator)
    t.start()

q = queueTickers()
while not q.empty() and ind:
    currentTicker = q.get()
    x = list(db.getFromPeriod(currentTicker, start, end))
    indicator_queue.put((x,currentTicker))

db.disconnect()

# x = json.loads(file)
# for days in x['candles']:
#     #day = days['candles']
#     open = days['open']
#     high = days['high']
#     timestmap = days['datetime'] / 1000
#     print(timestmap)
#     x = datetime.datetime.utcfromtimestamp(timestmap).strftime('%Y-%m-%d %H:%M:%S')
#     #x =  datetime.datetime.fromtimestamp(timestmap).strftime('%c')
#     print(x)

#print(response.text)