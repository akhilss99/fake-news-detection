from xmlrpc import server
import pandas as pd
import numpy as np
from CrawlerUtil import CrawlerUtility
import pyodbc
import json

class DatabaseUtility:
    
    def __init__(self, config=None):
        self.config = config
        f = open("config.json")
        self.password = json.load(f).get('password')
        connectionString = "Driver={ODBC Driver 13 for SQL Server};Server=tcp:newsdb-server.database.windows.net,1433;Database=newsdb;Uid=akhil;Pwd="+self.password+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Charset=utf8;Auto Translate = False;"
        self.conn = pyodbc.connect(connectionString)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT @@version;") 
        row = self.cursor.fetchone() 
        while row: 
            print(row[0])
            row = self.cursor.fetchone()
    
    def getCurrentData(self):
        end = 10000000000000000000000000000000
        oneindianews, oneindialabel = CrawlerUtility.oneindiascrape(1, 2)
        samayamnews, samayamlabel = CrawlerUtility.samayamscrape(1, 2)
        news18news, news18label = CrawlerUtility.news18scrape(1, 2)

        oneindiaData = {'News':oneindianews, 'Label':oneindialabel}
        samayamData = {'News':samayamnews, 'Label':samayamlabel}
        news18Data = {'News':news18news, 'Label':news18label}

        one_india = pd.DataFrame(oneindiaData)
        samayam = pd.DataFrame(samayamData)
        news18 = pd.DataFrame(news18Data)

        print('One_india: ',one_india.count())
        print('samayam: ',samayam.count())
        print('news18: ',news18.count())

        total = one_india.append(samayam, ignore_index = True)
        total = total.append(news18, ignore_index = True)

        df = total.sample(frac=1).reset_index(drop=True)
        print(df)
        return df

    def existingData(self):
        query = "SELECT * FROM dbo.News"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while(row):
            print(row[0]," ",row[1])
            row = self.cursor.fetchone()
        

    def writeData(self):
        self.clearDB()
        currentData = self.getCurrentData()
        print('Writing data...')
        for index, row in currentData.iterrows():
            insertQuery = "INSERT INTO dbo.News values("+row.News+","+row.Label+")"
            print(insertQuery)
            self.cursor.execute(insertQuery)
        self.conn.commit()

    def clearDB(self):
        self.delQuery = "DELETE FROM dbo.News;"
        self.cursor.execute(self.delQuery)

    
    def getNewData(self):
        currentData = self.getCurrentData()
        existingData = self.existingData()
        newData = currentData[~currentData.News.isin(existingData.News)]
        self.writeData(currentData)
        return newData

dbutil = DatabaseUtility()
dbutil.writeData()