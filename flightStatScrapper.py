#https://www.flightstats.com/v2/flight-tracker/departures/ATL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from holidayMethods import holidayPopulate
from DateAnalyzer import dateAnalyzer
import array as arr
import time 
from datetime import date
import schedule




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
    file.write("Date, Month, Day Of Week, Departure Time, Arrival Time, Flight Info, Destination, Airline Info, Holiday\n")
    file.close()

def addDataToCSV(fname, dataToAdd):
    dateAnalyzeT = dateAnalyzer(str(date.today()), '05:02')
    HolidayStatus = holidayPopulate(str(date.today()))
    dataToAdd.sort()
    file = open(fname, "a")
    for element in dataToAdd:
        line = '{},{},{},{},{},{},{},{}, {}\n'.format(str(date.today()), str(dateAnalyzeT[1]), str(dateAnalyzeT[0]), str(element[0]), str(element[1]), str(element[2]), str(element[3]), str(element[4]), str(HolidayStatus[0]))
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

#createNewCSV("data1.csv")
addDataToCSV("data2.csv", departureData)

time.sleep(2)
driver.quit()

    

