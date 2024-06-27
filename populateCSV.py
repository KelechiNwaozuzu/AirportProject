from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import requests
import pandas as pd
import time
import datetime
from datetime import timedelta
import requests
import pandas as pd
import requests
import pandas as pd
from io import StringIO
import os
import subprocess
import smtplib
from email.mime.text import MIMEText










# This file states the process of data collection for our model.

# This method scrapes FlightStats at 12:01 AM to collect the daily flight departure information.
# Used directly for: flight volume, and flight zoning.
def flightDepartureScraper():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.flightstats.com/v2/flight-tracker/departures/ATL")
    departureData = []



    def cookieAccepter():
        accept = driver.find_element(by=By.ID, value="onetrust-close-btn-container")
        accept.click()
    def tidyData(lineData):
        splitLinedata = lineData.split(" ")
        flightInfo = splitLinedata[0] + " " + splitLinedata[1]
        departureTime = splitLinedata[2]
        arrivalTime = splitLinedata[3]
        Destination = splitLinedata[-1]
        stringBuilder = ""
        if ("/" not in splitLinedata):
            for i in range(5, len(splitLinedata) - 1):
                stringBuilder += splitLinedata[i] + " "
            stringBuilder.strip()
            airlineInfo = stringBuilder.replace(",", "/")  
        else:
            slashIndex = splitLinedata.index("/")
            array1 = splitLinedata[5:slashIndex]
            for element in array1:
                stringBuilder += element + " "
            stringBuilder.strip() 
            airlineInfo = stringBuilder.replace(",", "/")  
        finalArray = [departureTime, arrivalTime, flightInfo, Destination, airlineInfo]
        return finalArray
    def getSubPages(): 
        paginationBar = driver.find_element(by=By.XPATH, value = "/html/body/div[1]/div/section/div/div[2]/div[3]/div")
        value = ""
        iterator = 3
        count = -1
        while(value != ("→")):
            currentElement = driver.find_element(by=By.XPATH, value = "/html/body/div[1]/div/section/div/div[2]/div[3]/div/div[{}]".format(iterator))
            value = currentElement.text
            count += 1
            iterator += 1
        return count
    def time0to6():
        timePeriodButton = driver.find_element(by=By.NAME, value="time")
        selecter = Select(timePeriodButton)
        selecter.select_by_value("0")
        filterbutton = driver.find_element(By.CLASS_NAME, "basic-button__Button-sc-3qdr1i-0.kmYwtt")
        filterbutton.click()
        time.sleep(1)


    def time6to12():
        timePeriodButton = driver.find_element(by=By.NAME, value="time")
        selecter = Select(timePeriodButton)
        selecter.select_by_value("6")
        filterbutton = driver.find_element(By.CLASS_NAME, "basic-button__Button-sc-3qdr1i-0.kmYwtt")
        filterbutton.click()
        time.sleep(1)


    def time12to18():
        timePeriodButton = driver.find_element(by=By.NAME, value="time")
        selecter = Select(timePeriodButton)
        selecter.select_by_value("12")
        filterbutton = driver.find_element(By.CLASS_NAME, "basic-button__Button-sc-3qdr1i-0.kmYwtt")
        filterbutton.click()
        time.sleep(1)

    def time18to24():
        timePeriodButton = driver.find_element(by=By.NAME, value="time")
        selecter = Select(timePeriodButton)
        selecter.select_by_value("18")
        filterbutton = driver.find_element(By.CLASS_NAME, "basic-button__Button-sc-3qdr1i-0.kmYwtt")
        filterbutton.click()
        time.sleep(1)
    
    def mainScraper():
        pagesToGoThrough = getSubPages()
        for x in range(0, pagesToGoThrough):
            table = driver.find_element(by=By.XPATH, value = "/html/body/div[1]/div/section/div/div[2]/div[2]")
            arrayData = table.text.split("\n")
            lengthOfRows = (int)(len(arrayData[4:]) / 6) + 2
            #DIVIDE ARRAY LENGTH BY 6 TO GET EACH INDIVIDUAL LENGTH
            for i in range(2, int(lengthOfRows)):
                #rowElement = driver.find_element(by=By.XPATH, value = "/html/body/div[1]/div/section/div/div[2]/div[2]/a[{}]".format(i))
                rowElement = driver.find_element(by=By.XPATH, value="//div[@id='__next']/div/section/div/div[2]/div[2]/a[{}]".format(i))
                stringLine = rowElement.text.replace("\n", " ")
                newrow = tidyData(stringLine)
                if newrow != None and len(newrow) == 5:
                    departureData.append(newrow)
            nextButton = driver.find_element(by=By.XPATH, value = "/html/body/div[1]/div/section/div/div[2]/div[3]/div/div[{}]".format(pagesToGoThrough + 3))
            nextButton.click()
    def createNewCSV(fname):
        file = open(fname, "w")
        file.write("Date, Departure Time, Arrival Time, Flight Info, Destination, Airline Info\n")
        file.close()

    def addDataToCSV(fname, dataToAdd):
        dataToAdd.sort()
        file = open(fname, "a")
        for element in dataToAdd:
            line = '{},{},{},{},{}, {}\n'.format(str(date.today()), str(element[0]), str(element[1]), str(element[2]), str(element[3]), str(element[4]))
            file.write(line)
        file.close()

    cookieAccepter()
    time0to6()
    mainScraper()
    time6to12()
    mainScraper()
    time12to18()
    mainScraper()
    time18to24()
    mainScraper()

    createNewCSV("todaysDepartures.csv")
    addDataToCSV("TodaysDepartures.csv", departureData)

    time.sleep(2)
    driver.quit()
    return

# This method scrapes the live wait times at the current time (time of row entry).
def getCurrentWaitTimes():
    proxy_address = "83.149.70.159"
    proxy_port = "13012"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.atl.com/times/")
    options.add_argument(f'--proxy-server={proxy_address}:{proxy_port}')
    # select elements by class name 
    try:
        elements = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "nesclasser2"))
        ).text
    except Exception as e:
        print(f"Timed out waiting for page to load: {e} at time: " + str(datetime.datetime.now()))
        return ["", "", "", "", ""]
    elementArr = elements.split()
    main_CHECKPOINT = elementArr[3]
    north_CHECKPOINT = elementArr[6]
    lower_NORTH_CHECKPOINT = elementArr[10]
    south_PRECHECK_ONLY_CHECKPOINT = elementArr[15]
    international_CHECKPOINT = elementArr[19]
    driver.close()
    #print('{} | {} | {} | {} | {}'.format(main_CHECKPOINT, north_CHECKPOINT, lower_NORTH_CHECKPOINT, south_PRECHECK_ONLY_CHECKPOINT, international_CHECKPOINT))
    return [main_CHECKPOINT, north_CHECKPOINT, lower_NORTH_CHECKPOINT, south_PRECHECK_ONLY_CHECKPOINT, international_CHECKPOINT]

def getFlightZoning():
    current_time = datetime.datetime.now()
    timeNow = str(current_time.strftime("%H%M"))

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
    if int(timeNow) >= 300 and int(timeNow) <= 2100:
        threeHoursAgo = (current_time - timedelta(hours=3)).strftime("%H:%M")
        threeHoursfromNow = (current_time + timedelta(hours=3)).strftime("%H:%M")
        return getNumberOf('todaysDepartures.csv', threeHoursAgo, threeHoursfromNow)
    elif int(timeNow) < 300:
        threeHoursAgo = (current_time - timedelta(hours=3)).strftime("%H:%M")
        threeHoursfromNow = (current_time + timedelta(hours=3)).strftime("%H:%M")
        yesterday = date.today() - timedelta(days=1)
        return getNumberOf('yesterdayDepatures.CSV', threeHoursAgo, '23:59', str(yesterday)) + getNumberOf('todaysDepartures.csv', '00:00', threeHoursfromNow)
    elif int(timeNow) > 2100:
        threeHoursAgo = (current_time - timedelta(hours=3)).strftime("%H:%M")
        return getNumberOf('todaysDepartures.csv', threeHoursAgo, '23:59')
    



# This method gets the live weather at the current time (e.g., precipitation, temperature, etc.).
def getCurrentWeather():
    weatherCode = {
      "0": "Unknown",
      "1000": "Clear, Sunny",
      "1100": "Mostly Clear",
      "1101": "Partly Cloudy",
      "1102": "Mostly Cloudy",
      "1001": "Cloudy",
      "1103": "Partly Cloudy and Mostly Clear",
      "2100": "Light Fog",
      "2101": "Mostly Clear and Light Fog",
      "2102": "Partly Cloudy and Light Fog",
      "2103": "Mostly Cloudy and Light Fog",
      "2106": "Mostly Clear and Fog",
      "2107": "Partly Cloudy and Fog",
      "2108": "Mostly Cloudy and Fog",
      "2000": "Fog",
      "4204": "Partly Cloudy and Drizzle",
      "4203": "Mostly Clear and Drizzle",
      "4205": "Mostly Cloudy and Drizzle",
      "4000": "Drizzle",
      "4200": "Light Rain",
      "4213": "Mostly Clear and Light Rain",
      "4214": "Partly Cloudy and Light Rain",
      "4215": "Mostly Cloudy and Light Rain",
      "4209": "Mostly Clear and Rain",
      "4208": "Partly Cloudy and Rain",
      "4210": "Mostly Cloudy and Rain",
      "4001": "Rain",
      "4211": "Mostly Clear and Heavy Rain",
      "4202": "Partly Cloudy and Heavy Rain",
      "4212": "Mostly Cloudy and Heavy Rain",
      "4201": "Heavy Rain",
      "5115": "Mostly Clear and Flurries",
      "5116": "Partly Cloudy and Flurries",
      "5117": "Mostly Cloudy and Flurries",
      "5001": "Flurries",
      "5100": "Light Snow",
      "5102": "Mostly Clear and Light Snow",
      "5103": "Partly Cloudy and Light Snow",
      "5104": "Mostly Cloudy and Light Snow",
      "5122": "Drizzle and Light Snow",
      "5105": "Mostly Clear and Snow",
      "5106": "Partly Cloudy and Snow",
      "5107": "Mostly Cloudy and Snow",
      "5000": "Snow",
      "5101": "Heavy Snow",
      "5119": "Mostly Clear and Heavy Snow",
      "5120": "Partly Cloudy and Heavy Snow",
      "5121": "Mostly Cloudy and Heavy Snow",
      "5110": "Drizzle and Snow",
      "5108": "Rain and Snow",
      "5114": "Snow and Freezing Rain",
      "5112": "Snow and Ice Pellets",
      "6000": "Freezing Drizzle",
      "6003": "Mostly Clear and Freezing drizzle",
      "6002": "Partly Cloudy and Freezing drizzle",
      "6004": "Mostly Cloudy and Freezing drizzle",
      "6204": "Drizzle and Freezing Drizzle",
      "6206": "Light Rain and Freezing Drizzle",
      "6205": "Mostly Clear and Light Freezing Rain",
      "6203": "Partly Cloudy and Light Freezing Rain",
      "6209": "Mostly Cloudy and Light Freezing Rain",
      "6200": "Light Freezing Rain",
      "6213": "Mostly Clear and Freezing Rain",
      "6214": "Partly Cloudy and Freezing Rain",
      "6215": "Mostly Cloudy and Freezing Rain",
      "6001": "Freezing Rain",
      "6212": "Drizzle and Freezing Rain",
      "6220": "Light Rain and Freezing Rain",
      "6222": "Rain and Freezing Rain",
      "6207": "Mostly Clear and Heavy Freezing Rain",
      "6202": "Partly Cloudy and Heavy Freezing Rain",
      "6208": "Mostly Cloudy and Heavy Freezing Rain",
      "6201": "Heavy Freezing Rain",
      "7110": "Mostly Clear and Light Ice Pellets",
      "7111": "Partly Cloudy and Light Ice Pellets",
      "7112": "Mostly Cloudy and Light Ice Pellets",
      "7102": "Light Ice Pellets",
      "7108": "Mostly Clear and Ice Pellets",
      "7107": "Partly Cloudy and Ice Pellets",
      "7109": "Mostly Cloudy and Ice Pellets",
      "7000": "Ice Pellets",
      "7105": "Drizzle and Ice Pellets",
      "7106": "Freezing Rain and Ice Pellets",
      "7115": "Light Rain and Ice Pellets",
      "7117": "Rain and Ice Pellets",
      "7103": "Freezing Rain and Heavy Ice Pellets",
      "7113": "Mostly Clear and Heavy Ice Pellets",
      "7114": "Partly Cloudy and Heavy Ice Pellets",
      "7116": "Mostly Cloudy and Heavy Ice Pellets",
      "7101": "Heavy Ice Pellets",
      "8001": "Mostly Clear and Thunderstorm",
      "8003": "Partly Cloudy and Thunderstorm",
      "8002": "Mostly Cloudy and Thunderstorm",
      "8000": "Thunderstorm"
    }
    url = "https://api.tomorrow.io/v4/weather/realtime"

    params = {
        "location": "33.753746,-84.386330",  
        "units": "imperial",
        "apikey": "E0oe3K6YxiPv7sHqllVS5ir0bEnHWt8j"
    }

    response = requests.get(url, params=params)
    data = response.json()
    #print(data)

    weather_data = {
        'temperature': data['data']['values']['temperature'],
        'weathercode': data['data']['values']['weatherCode'],
        'precProb': data['data']['values']['precipitationProbability']
    }

    return '{} | {} | {}'.format(weather_data['temperature'], weather_data['weathercode'], weather_data['precProb'])

# This method gets the day of the month at the time of execution.
def getMonth():
    time_str = '12:00'
    date_str = str(date.today())
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    day_of_week = date_obj.isoweekday()
    month = date_obj.month
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    military_time = time_obj.strftime("%H%M")
    result_tuple = (day_of_week, month, int(military_time))
    return result_tuple[1]


def createYesterdayCSV():
    infile = open('todaysDepartures.csv', 'r')
    outfile = open('yesterdayDepatures.CSV', "w")
    data = infile.read()
    infile.close()
    outfile.write(data)
    outfile.close()
    return
    

# This method gets the day of the week at the time of execution.
def getDayOfWeek():
    date_str = str(date.today())
    time_str = '12:00'
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    day_of_week = date_obj.isoweekday()
    month = date_obj.month
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    military_time = time_obj.strftime("%H%M")
    result_tuple = (day_of_week, month, int(military_time))
    return result_tuple[0]

# This method gets information on the traffic at each terminal at the time of execution.
def getAllTerminalTraffic():
    API_KEY = 'AEUHufdwQn2JwytsieIA18AD0uTJegKo'
    URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}&point=33.64117,-84.44361" 
    response = requests.get(URL)

    params = {
        'unit': 'mph',
    }

    if response.status_code == 200:
        data = response.json()
        # Extract traffic data from the response
        domestic = str(data['flowSegmentData']['currentSpeed']) + " | " + str(data['flowSegmentData']['currentTravelTime'])

        URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}&point=33.6412,-84.41972" 
        response = requests.get(URL)
        params = {
        'unit': 'mph',
        }  
        international = str(data['flowSegmentData']['currentSpeed']) + " | " + str(data['flowSegmentData']['currentTravelTime'])
    else:
        print(f"Error: {response.status_code}")
     



    return [domestic, international]

# This method returns 0 or 1 depending on whether the current day is a holiday.
def holidayStatus(date):
    holidayData = [{'date': '2024-01-01', 'localName': "New Year's Day", 'name': "New Year's Day", 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-01-15', 'localName': 'Martin Luther King, Jr. Day', 'name': 'Martin Luther King, Jr. Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-02-19', 'localName': "Washington's Birthday", 'name': 'Presidents Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-03-29', 'localName': 'Good Friday', 'name': 'Good Friday', 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-CT', 'US-DE', 'US-HI', 'US-IN', 'US-KY', 'US-LA', 'US-NC', 'US-ND', 'US-NJ', 'US-TN'], 'launchYear': None, 'types': ['Public']}, {'date': '2024-03-29', 'localName': 'Good Friday', 'name': 'Good Friday', 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-TX'], 'launchYear': None, 'types': ['Optional']}, {'date': '2024-05-27', 'localName': 'Memorial Day', 'name': 'Memorial Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-06-19', 'localName': 'Juneteenth National Independence Day', 'name': 'Juneteenth National Independence Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-07-04', 'localName': 'Independence Day', 'name': 'Independence Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-09-02', 'localName': 'Labour Day', 'name': 'Labor Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-10-14', 'localName': 'Columbus Day', 'name': 'Columbus Day', 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-AL', 'US-AZ', 'US-CO', 'US-CT', 'US-GA', 'US-ID', 'US-IL', 'US-IN', 'US-IA', 'US-KS', 'US-KY', 'US-LA', 'US-ME', 'US-MD', 'US-MA', 'US-MS', 'US-MO', 'US-MT', 'US-NE', 'US-NH', 'US-NJ', 'US-NM', 'US-NY', 'US-NC', 'US-OH', 'US-OK', 'US-PA', 'US-RI', 'US-SC', 'US-TN', 'US-UT', 'US-VA', 'US-WV'], 'launchYear': None, 'types': ['Public']}, {'date': '2024-10-14', 'localName': "Indigenous Peoples' Day", 'name': "Indigenous Peoples' Day", 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-AK', 'US-AL', 'US-CA', 'US-HI', 'US-IA', 'US-LA', 'US-ME', 'US-MI', 'US-MN', 'US-NC', 'US-NE', 'US-NM', 'US-OK', 'US-OR', 'US-SD', 'US-TX', 'US-VA', 'US-VT', 'US-WI'], 'launchYear': None, 'types': ['Public']}, {'date': '2024-11-11', 'localName': 'Veterans Day', 'name': 'Veterans Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-11-28', 'localName': 'Thanksgiving Day', 'name': 'Thanksgiving Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-12-25', 'localName': 'Christmas Day', 'name': 'Christmas Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}]
    for holiday in holidayData:
        if (date == holiday['date']):
            return [1, holiday['localName']]
    return [0, ""]


# This method creates a new CSV file with the selected header. This should only be used once.
# @param fname: the name of the file you want to create.
def createCSV(fname):
    file = open(fname, "w")
    file.write("Date, Time of Scrape, Flight Zoning, MC, NC, LNC, SPOC, INTLC, Weather, Month, Day of Week, Holiday\n")
    file.close()
    print('New File has been created')
    return


def updateExistingCSV(fname):
    file = open(fname, "a")
    holidayValue = holidayStatus(str(date.today()))[0]
    current_time = datetime.datetime.now()
    timeNow = str(current_time.strftime("%H:%M:%S"))[0:5]
    flightZoneAmt = str(getFlightZoning())
    checkPointWaitList = getCurrentWaitTimes()
    file.write('{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(str(date.today()), timeNow, flightZoneAmt, checkPointWaitList[0], checkPointWaitList[1], checkPointWaitList[2], checkPointWaitList[3], checkPointWaitList[4], getCurrentWeather(), getMonth(), getDayOfWeek(), holidayValue))
    file.close()
    return


# This method uses the time module to automatically run and add a row of data to an existing
# CSV file every 15 minutes, starting at 12:15 AM.
def main():
    #createYesterdayCSV()
    #flightDepartureScraper()
    #createCSV('testRunV4.csv')
    #updateExistingCSV('testRunV4.csv')
    #getCurrentWaitTimes()

    
    try:
        while True:

            current_time = datetime.datetime.now()
            timeNow = str(current_time.strftime("%H:%M:%S"))
            if timeNow == '00:00:01':
                createYesterdayCSV()
                time.sleep(60)
                flightDepartureScraper()
                time.sleep(300)

            if timeNow in ['00:05:00', '00:10:00', '00:15:00', '00:20:00', '00:25:00', '00:30:00', '00:35:00', '00:40:00', '00:45:00', '00:50:00', '00:55:00', '01:00:00', '01:05:00'
                       , '01:10:00', '01:15:00', '01:20:00', '01:25:00', '01:30:00', '01:35:00', '01:40:00', '01:45:00', '01:50:00', '01:55:00', '02:00:00', '02:05:00', '02:10:00'
                       , '02:15:00', '02:20:00', '02:25:00', '02:30:00', '02:35:00', '02:40:00', '02:45:00', '02:50:00', '02:55:00', '03:00:00', '03:05:00', '03:10:00', '03:15:00'
                       , '03:20:00', '03:25:00', '03:30:00', '03:35:00', '03:40:00', '03:45:00', '03:50:00', '03:55:00', '04:00:00', '04:05:00', '04:10:00', '04:15:00', '04:20:00', '04:25:00'
                       , '04:30:00', '04:35:00', '04:40:00', '04:45:00', '04:50:00', '04:55:00', '05:00:00', '05:05:00', '05:10:00', '05:15:00', '05:20:00', '05:25:00', '05:30:00', '05:35:00', '05:40:00', '05:45:00'
                       , '05:50:00', '05:55:00', '06:00:00', '06:05:00', '06:10:00', '06:15:00', '06:20:00', '06:25:00', '06:30:00', '06:35:00', '06:40:00', '06:45:00', '06:50:00', '06:55:00', '07:00:00', '07:05:00'
                       , '07:10:00', '07:15:00', '07:20:00', '07:25:00', '07:30:00', '07:35:00', '07:40:00', '07:45:00', '07:50:00', '07:55:00', '08:00:00', '08:05:00', '08:10:00', '08:15:00', '08:20:00', '08:25:00'
                       , '08:30:00', '08:35:00', '08:40:00', '08:45:00', '08:50:00', '08:55:00', '09:00:00', '09:05:00', '09:10:00', '09:15:00', '09:20:00', '09:25:00', '09:30:00', '09:35:00', '09:40:00', '09:45:00'
                       , '09:50:00', '09:55:00', '10:00:00', '10:05:00', '10:10:00', '10:15:00', '10:20:00', '10:25:00', '10:30:00', '10:35:00', '10:40:00', '10:45:00', '10:50:00', '10:55:00', '11:00:00', '11:05:00'
                       , '11:10:00', '11:15:00', '11:20:00', '11:25:00', '11:30:00', '11:35:00', '11:40:00', '11:45:00', '11:50:00', '11:55:00', '12:00:00', '12:05:00', '12:10:00', '12:15:00', '12:20:00', '12:25:00'
                       , '12:30:00', '12:35:00', '12:40:00', '12:45:00', '12:50:00', '12:55:00', '13:00:00', '13:05:00', '13:10:00', '13:15:00', '13:20:00', '13:25:00', '13:30:00', '13:35:00', '13:40:00', '13:45:00'
                       , '13:50:00', '13:55:00', '14:00:00', '14:05:00', '14:10:00', '14:15:00', '14:20:00', '14:25:00', '14:30:00', '14:35:00', '14:40:00', '14:45:00', '14:50:00', '14:55:00', '15:00:00', '15:05:00'
                       , '15:10:00', '15:15:00', '15:20:00', '15:25:00', '15:30:00', '15:35:00', '15:40:00', '15:45:00', '15:50:00', '15:55:00', '16:00:00', '16:05:00', '16:10:00', '16:15:00', '16:20:00', '16:25:00'
                       , '16:30:00', '16:35:00', '16:40:00', '16:45:00', '16:50:00', '16:55:00', '17:00:00', '17:05:00', '17:10:00', '17:15:00', '17:20:00', '17:25:00', '17:30:00', '17:35:00', '17:40:00', '17:45:00'
                       , '17:50:00', '17:55:00' '18:00:00', '18:05:00', '18:10:00', '18:15:00', '18:20:00', '18:25:00', '18:30:00', '18:35:00', '18:40:00', '18:45:00', '18:50:00', '18:55:00', '19:00:00', '19:05:00'
                       , '19:10:00', '19:15:00', '19:20:00', '19:25:00', '19:30:00', '19:35:00', '19:40:00', '19:45:00', '19:50:00', '19:55:00', '20:00:00', '20:05:00', '20:10:00', '20:15:00', '20:20:00', '20:25:00'
                       , '20:30:00', '20:35:00', '20:40:00', '20:45:00', '20:50:00', '20:55:00', '21:00:00', '21:05:00', '21:10:00', '21:15:00', '21:20:00', '21:25:00', '21:30:00', '21:35:00', '21:40:00', '21:45:00'
                       , '21:50:00', '21:55:00', '22:00:00', '22:05:00', '22:10:00', '22:15:00', '22:20:00', '22:25:00', '22:30:00', '22:35:00', '22:40:00', '22:45:00', '22:50:00', '22:55:00', '23:00:00', '23:05:00'
                       , '23:10:00', '23:15:00', '23:20:00', '23:25:00', '23:30:00', '23:35:00', '23:40:00', '23:45:00', '23:50:00', '23:55:00']:
                if any(abs((current_time - datetime.datetime.combine(current_time.date(), datetime.time.fromisoformat(t))).total_seconds()) < 2 for t in target_times):
                    updateExistingCSV('testRunV3.csv')
                    print('CSV has been updated at: ' + timeNow)
            time.sleep(1)
    except:
        subject = "ERROR: CHECK CODE"
        body = "Python Script: POPULATECSV.py has STOPPED OPERATING PROPERLY. Check error and recompile!"
        sender = "sguexil@gmail.com" 
        recipients = ["sguexil@gmail.com", "teniojosipeofficial@gmail.com", "Jurmainmitchell05@gmail.com", "knwaozuzu@gmail.com", "tmonod01@gmail.com"]
        password = "llom dtvc libi cgqk"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")
    
            

main()