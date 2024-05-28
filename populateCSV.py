# This file states the process of data collected for our model.

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
def holidayStatus():
    return

# This method creates a new CSV file with the selected header. It should only be used once.
# @param fname: the name of the file you want to create.
def createCSV(fname):
    return

# This method uses the time module to automatically run and add a row of data to an existing
# CSV file every 15 minutes, starting at 12:15 AM.
def main():
    return