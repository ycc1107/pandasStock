import csv
import logging

class Date_Maker:
    BEFORE_MARKET = 'BTO'
    AFTER_MARKET = 'AMC'

class Col_Index:
    Ticker_INDEX = 1
    DATE_INDEX = 2
    ACT_RPT_CODE_INDEX = 10

def processRawData():
    with open('price.csv','r') as f:
        price_raw = []


    with open('eps.csv','r') as f:
        reader = csv.reader(f,delimiter=',')
        raw = [ (line[Col_Index.Ticker_INDEX],line[Col_Index.DATE_INDEX],line[Col_Index.ACT_RPT_CODE_INDEX]) for line in range(1,len(reader)) ]




    print raw[:10]


processRawData()