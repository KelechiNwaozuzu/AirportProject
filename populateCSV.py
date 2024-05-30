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
    return

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
    return

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
    file.write("Date, Time of Scrape, Flight Zoning, Live Security Wait Time, Weather, Month, Day of Week, Airline Info, Terminal Traffic, Holiday\n")
    file.close()
    print('New File has been created')
    return


def updateExistingCSV(fname):
    file = open(fname, "a")
    holidayValue = holidayStatus(str(date.today()))[0]
    current_time = datetime.datetime.now()
    timeNow = str(current_time.strftime("%H:%M:%S"))[0:5]
    file.write('{}, {},{},{},{},{},{},{},{},{}\n'.format(str(date.today()), timeNow, "", "", getCurrentWeather(), getMonth(), getDayOfWeek(), "", "", holidayValue,))
    file.close()
    return


# This method uses the time module to automatically run and add a row of data to an existing
# CSV file every 15 minutes, starting at 12:15 AM.
def main():
    #flightDepartureScraper()
    #createCSV('practice2.csv')
    updateExistingCSV('practice2.csv')

main()
