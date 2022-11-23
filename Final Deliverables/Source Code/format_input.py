import pandas as pd
from datetime import datetime
import calendar

days = {
    "Monday":1,
    "Tuesday":2,
    "Wednesday":3,
    "Thursday":4,
    "Friday":5,
    "Saturday":6,
    "Sunday":7
}

def extract_distance(src , dest):
    df = pd.read_csv('dataset/flightdata.csv')
    return df.loc[(df['ORIGIN']==src) & (df['DEST']==dest)]['DISTANCE'].to_numpy()[0]

def get_quater(month: int) -> int:
    res = 1
    while(month>3):
        res = res+1
        month-=3
    return res

def extract_date(date: str):
    x = []
    date = date.split("-")
    x.append(get_quater(int(date[1])))
    x.append(int(date[1]))
    x.append(int(date[2]))
    x.append(days[calendar.day_name[datetime(int(date[0]), int(date[1]), int(date[2])).weekday()]])
    return x