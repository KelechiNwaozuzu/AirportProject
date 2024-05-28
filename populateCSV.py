from datetime import date
import requests





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
    return

# This method gets the day of the month at the time of execution.
def getDayOfMonth():
    return

# This method gets the day of the week at the time of execution.
def getDayOfWeek():
    return

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
    file.write("Time of Scrape, Flight Volume, Flight Zoning, Live Security Wait Time, Weather, Month, Day of Week, Airline Info, Terminal Traffic, Holiday\n")
    file.close()
    print('New File has been created')
    return


def updateExistingCSV(fname):
    file = open(fname, "a")
    holidayValue = holidayStatus(str(date.today()))[0]
    file.write('{},{},{},{},{},{},{},{},{}, {}'.format("", "", "", "", "", "", "", "", "", holidayValue,))
    return


# This method uses the time module to automatically run and add a row of data to an existing
# CSV file every 15 minutes, starting at 12:15 AM.
def main():
    return

main()
