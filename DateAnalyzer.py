import pandas as pd
import time
import datetime
from datetime import date

def dateAnalyzer(date_str, time_str):
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    day_of_week = date_obj.isoweekday()

    month = date_obj.month

    time_obj = datetime.datetime.strptime(time_str, "%H:%M")

    military_time = time_obj.strftime("%H%M")

    result_tuple = (day_of_week, month, int(military_time))

    return result_tuple

date_dict = {}

df = pd.read_csv('content/drive/MyDrive/AirportProject/Data.csv')

def addRowToDict(row):
    date_str = row['Date']
    dep_time_str = row['Departure Time']
    
    result_tuple = dateAnalyzer(date_str, dep_time_str)

    key = data_str + ' ' + dep_time_str

    date_dict[key] = result_tuple

df.apply(addRowToDict, axis=1)
print(date_dict) # prints numerical day of week, numerical month, time (in order)
output_csv_file_path = '/content/drive/MyDrive/AirportProject/UpdatedData.csv'
df.to_csv(output_csv_file_path, index=False)
