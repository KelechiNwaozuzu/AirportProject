
#Reads the file and returns the data in the form of a list!

def fileRead(fname):
    with open(fname, 'r') as file:
        header = file.readline().strip()  # Read and strip the header line
        dataList = file.readlines()  # Read the rest of the lines
    dataList = [line.strip().split(',') for line in dataList]
    currentIndex = len(dataList) + 1 #+1 counting the header
    return dataList


#edits and remakes the data list into numerical values!
#Creates a new list that ignores any type of infomration that can't be quantified into numbers.
def dataRemake(dataList):
    dataListv2 = []
    for data in dataList:
        time = data[1].replace(":", "")
        temp = data[8].split(" | ")[0]
        poP = data[8].split(" | ")[2]
        processed_data = [float(time), float(data[2]), float(data[3]), float(data[4]), float(data[5]), float(data[6]), float(data[7]), float(temp), float(poP), float(data[9]), float(data[10]), float(data[11])]
        dataListv2.append(processed_data)
    return dataListv2

#This value gets the maximum of each variable (last 3 is month, day of week, and holiday status!)
def getMaximums(dataList):
    maxValues = []
    timeScrape = [int(row[0]) for row in dataList]
    maxTimeScrape = max(timeScrape)
    maxValues.append(maxTimeScrape)
    
    zone = [int(row[1]) for row in dataList]
    maxZone = max(zone)
    maxValues.append(maxZone)

    mainC = [int(row[2]) for row in dataList]
    maxMainC = max(mainC)
    maxValues.append(maxMainC)

    northC = [int(row[3]) for row in dataList]
    maxNorthC = max(northC)
    maxValues.append(maxNorthC)

    lNorthC = [int(row[4]) for row in dataList]
    maxlNorthC = max(lNorthC)
    maxValues.append(maxlNorthC)

    spoC = [int(row[5]) for row in dataList]
    maxspoC = max(spoC)
    maxValues.append(maxspoC)

    intlC = [int(row[6]) for row in dataList]
    maxintlC = max(intlC)
    maxValues.append(maxintlC)

    weather = [int(row[7]) for row in dataList]
    maxWeather = max(weather)
    maxValues.append(maxWeather)

    poP = [int(row[8]) for row in dataList]
    maxpoP = max(poP)
    maxValues.append(maxpoP)
    maxValues.append(12)
    maxValues.append(7)
    maxValues.append(1)

    return maxValues

#divides the column by the max and changes the value!
def normalizer(maxValues, dataListv2):
    for data in dataListv2:
        for i in range(12):
            data[i] = round(data[i] / maxValues[i], 4)
    print(dataListv2[0])



    


normalizer(getMaximums(dataRemake(fileRead('testRunV4.csv'))),  dataRemake(fileRead('testRunV4.csv')))