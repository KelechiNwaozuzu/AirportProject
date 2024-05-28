from datetime import date
import requests





# This file states the process of data collection for our model.

# This method scrapes FlightStats at 12:01 AM to collect the daily flight departure information.
# Used directly for: flight volume, and flight zoning.
def flightDepartureScraper():
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


# This method creates a new CSV file with the selected header. This should only be used once.
# @param fname: the name of the file you want to create.
def createCSV(fname):
    file = open(fname, "w")
    file.write("Time of Scrape, Flight Volume, Flight Zoning, Live Security Wait Time, Weather, Month, Day of Week, Airline Info, Terminal Traffic, Holiday\n")
    file.close()
    print('New File has been created')
    return


def updateExistingCSV(fname):
    return


# This method uses the time module to automatically run and add a row of data to an existing
# CSV file every 15 minutes, starting at 12:15 AM.
def main():
    #createCSV('practice.csv')
    holidayStatus('2024-05-27')
    return

main()
