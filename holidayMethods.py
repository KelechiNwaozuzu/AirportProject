import requests
from DateAnalyzer import dateAnalyzer 
import DateAnalyzer
from datetime import date
# parameters--> String date: represents a string of the date in this 'yyyy-mm-dd' format
# returns: a list returning 0(false) or 1(true) if there is a holiday, and the holiday names.
#i.e 2024-01-01 ----> [1, ['New Year's Day']]
#API has major trouble with large request, so a dictionary is saved in this file 

"""
We need to find a way to update change date if api is in the correct year
"""


def getHolidayAPIData(date):
    response = requests.get("https://date.nager.at/api/v3/PublicHolidays/{}/{}".format(2024, 'US'))
    data = response.json()
    return data


def holidayFinder(date, holidayData):
    for holiday in holidayData:
        if (date == holiday['date']):
            return [1, holiday['localName']]
    return [0, 'None']

def holidayPopulate(dateInput):
    holidayData = [{'date': '2024-01-01', 'localName': "New Year's Day", 'name': "New Year's Day", 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-01-15', 'localName': 'Martin Luther King, Jr. Day', 'name': 'Martin Luther King, Jr. Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-02-19', 'localName': "Washington's Birthday", 'name': 'Presidents Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-03-29', 'localName': 'Good Friday', 'name': 'Good Friday', 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-CT', 'US-DE', 'US-HI', 'US-IN', 'US-KY', 'US-LA', 'US-NC', 'US-ND', 'US-NJ', 'US-TN'], 'launchYear': None, 'types': ['Public']}, {'date': '2024-03-29', 'localName': 'Good Friday', 'name': 'Good Friday', 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-TX'], 'launchYear': None, 'types': ['Optional']}, {'date': '2024-05-27', 'localName': 'Memorial Day', 'name': 'Memorial Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-06-19', 'localName': 'Juneteenth National Independence Day', 'name': 'Juneteenth National Independence Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-07-04', 'localName': 'Independence Day', 'name': 'Independence Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-09-02', 'localName': 'Labour Day', 'name': 'Labor Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-10-14', 'localName': 'Columbus Day', 'name': 'Columbus Day', 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-AL', 'US-AZ', 'US-CO', 'US-CT', 'US-GA', 'US-ID', 'US-IL', 'US-IN', 'US-IA', 'US-KS', 'US-KY', 'US-LA', 'US-ME', 'US-MD', 'US-MA', 'US-MS', 'US-MO', 'US-MT', 'US-NE', 'US-NH', 'US-NJ', 'US-NM', 'US-NY', 'US-NC', 'US-OH', 'US-OK', 'US-PA', 'US-RI', 'US-SC', 'US-TN', 'US-UT', 'US-VA', 'US-WV'], 'launchYear': None, 'types': ['Public']}, {'date': '2024-10-14', 'localName': "Indigenous Peoples' Day", 'name': "Indigenous Peoples' Day", 'countryCode': 'US', 'fixed': False, 'global': False, 'counties': ['US-AK', 'US-AL', 'US-CA', 'US-HI', 'US-IA', 'US-LA', 'US-ME', 'US-MI', 'US-MN', 'US-NC', 'US-NE', 'US-NM', 'US-OK', 'US-OR', 'US-SD', 'US-TX', 'US-VA', 'US-VT', 'US-WI'], 'launchYear': None, 'types': ['Public']}, {'date': '2024-11-11', 'localName': 'Veterans Day', 'name': 'Veterans Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-11-28', 'localName': 'Thanksgiving Day', 'name': 'Thanksgiving Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}, {'date': '2024-12-25', 'localName': 'Christmas Day', 'name': 'Christmas Day', 'countryCode': 'US', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'types': ['Public']}]
    if holidayData[0]['date'][:4] != str(date.today())[:4]:
        holidayData = getHolidayAPIData(date.today())
    else:
        return holidayFinder(dateInput, holidayData)

#This method fixes csvs by returning a new csv with updated formating.
#Ignore this method unless you want to make holday and Datechanges to CSV
#makes a new csv!

def csvVersion2Update(fname):
    file = open('data.csv', "r")
    header = file.readline()
    data = file.readlines()
    file.close


    


    outputFile = open(fname, "w")
    outputFile.write("Date, Month, Day Of Week, Departure Time, Arrival Time, Flight Info, Destination, Airline Info, Holiday\n")

    buildData = []
    for dataline in data:
        splitData = dataline.strip().split(',')
        date = splitData[0]
        dTime = splitData[1]
        aTime = splitData[2]
        fInfo = splitData[3]
        Dest = splitData[4]
        airL = splitData[5]
        dateAnalyzeT = dateAnalyzer(date, '05:02')
        HolidayStatus = holidayPopulate(date)
        buildData += [date, dateAnalyzeT[1], dateAnalyzeT[0], dTime, aTime, fInfo, Dest, airL, HolidayStatus[0]]
        outputFile.write('{},{},{},{},{},{},{},{}, {}\n'.format(str(date), str(dateAnalyzeT[1]), str(dateAnalyzeT[0]), str(dTime), str(aTime), str(fInfo), str(Dest), str(airL), str(HolidayStatus[0])))
    outputFile.close()
    print('CSV has successfully processed!')


#print(holidayFinder('2024-01-01'))
csvVersion2Update('data2.csv')



