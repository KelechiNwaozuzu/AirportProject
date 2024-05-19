import time 
import datetime
from datetime import date
from holidayMethods import csvVersion2Update
#Gets number of flights given a csv file to read, a start time [incluive], an end time [inclusive], and the date.
#date MUST be in 'yyyy-mm-dd' format, if you want to read data from today, leave date empty!
#insert time values as normal in string format.
#EXAMPLE: getNumberOf('data.csv', '11:00', '11:60', '2024-05-10')
def getNumberOf(fname, start, end, dateInput = str(date.today())):
    
    sameDateList = []
    inRangeList = []

    if fname == None:
        print("File name cannot be null")
        return 0
    file = open(fname, "r")
    header  = file.readline()
    dataList = file.readlines()
    file.close()
    for element in dataList:
        elementList = element.strip().split(",")
        #invokes date filter
        if elementList[0] == dateInput:
            sameDateList.append(elementList)
        #start/end filter
    for elementList in sameDateList:
        time = int(elementList[1].replace(":", ""))
        startInt = int(start.replace(":", ""))
        endInt = int(end.replace(":", ""))
        if time >= startInt and time <= endInt:
            inRangeList.append(elementList)     
    if len(sameDateList) == 0:
        print("No data present for given date! **check format in docs**")
        return 0
    if len(inRangeList) == 0:
        print("No such data in given range")
        return 0
    return (len(inRangeList))
    
#HELPER METHOD.. IGNORE
def addMinutesToTime(military_time, minutes_to_add):
    hours, minutes = map(int, military_time.split(':'))
    total_minutes = hours * 60 + minutes
    total_minutes += int(minutes_to_add)  # Ensure minutes_to_add is an integer
    total_minutes %= 24 * 60
    new_hours = total_minutes // 60
    new_minutes = total_minutes % 60
    result = '{:02d}:{:02d}'.format(new_hours, new_minutes)
    return result

#Uses getNumberOf() to invoke the number of flights, where fromNow is minutes (integer)
# NOTE: can also work if the time  DOES NOT falls over to the next day. 
# EXAMPLE: getNumberOfFromNow('data.csv' fromNow)--> returns 
def getNumberOfFromNow(fname, fromNow):
    if fname == None or fname == "":
        print("Error: File name can not be null")
    currentTimeStr = datetime.datetime.now()
    currentTimeStr = str(currentTimeStr)[11:16]
    endtime = addMinutesToTime(currentTimeStr, fromNow)

    
    if int(endtime.replace(":", "")) <= 2359 and int(currentTimeStr.replace(":", "") <= endtime):
        return getNumberOf(fname, currentTimeStr, endtime)
    #CHECK NOTE
    else:
        print("Multi-day collection is not allowed for methods using currentDay!")
        return 0

    

    
    



#print(getNumberOf('data.csv', '0:00', '23:59', '2024-05-10'))
#print(getNumberOf('data.csv', '18:49', '18:59', '2024-05-12'))
print(getNumberOfFromNow("Data.csv", 100))

