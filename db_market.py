import pymysql
import datetime
# -*- coding: utf-8 -*-
import re
import calendar
import operator
import os
from collections import defaultdict
import json
class market():
    def __init__(self):
        #self.dbTable = table

        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='Trock!123',
                                          db='market')
        self.cursorObject = self.connection.cursor()
    def setTicker(self,ticker):
        self.ticker = ticker
    def disconnect(self):
        self.connection.close()

    def doesTableExist(self,tablename):
        query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'".format(tablename)

        self.cursorObject.execute(query)
        if self.cursorObject.fetchone()[0] == 1:
            print("exists")
            return True

        print("false")
        return False
    def insertResults(self,re):
        results = json.loads(re)
        print(len(results['candles']))
        for days in results['candles']:
            # day = days['candles']
            open = float(days['open'])
            high = float(days['high'])
            low = float(days['low'])
            close = float(days['close'])
            volume = int(days['volume'])
            timestmap = days['datetime'] / 1000

            timestmap = datetime.datetime.fromtimestamp(timestmap).strftime('%Y-%m-%d %H:%M:%S')

        #print(days)
            insert_post = "INSERT IGNORE INTO {} " \
                      "(open,high,low,close,volume,timestamp)" \
                      "VALUES ({},{},{},{},{},{});".format(self.ticker,open,high,low,close,volume,'"{}"'.format(timestmap))
            self.cursorObject.execute(insert_post)
        self.connection.commit()

    def printResponse(self,re):
        results = json.loads(re)
        for days in results['candles']:
            print(days)
    def getLastUpdated(self,ticker):
        query = 'SELECT timestamp FROM {} ORDER BY ID DESC LIMIT 1'.format(ticker)
        self.cursorObject.execute(query)
        return self.cursorObject.fetchone()

    def getFromPeriod(self,ticker,start,end):
        query = 'select * from {} where timestamp >="{}"  and timestamp <="{}"'.format(ticker,start,end)
        self.cursorObject.execute(query)
        return self.cursorObject.fetchall();
    def createTable(self,ticker):
        query = 'CREATE TABLE {}(ID int NOT NULL AUTO_INCREMENT,open float,high float,low float,close float,volume int,timestamp datetime,PRIMARY KEY (ID))'.format(ticker)
        self.cursorObject.execute(query)

