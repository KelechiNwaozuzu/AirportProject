
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
        try:
            time = data[1].replace(":", "")
            temp = data[8].split(" | ")[0]
            poP = data[8].split(" | ")[2]
            processed_data = [
                float(time) if time else 0.0,
                float(data[2]) if data[2] else 0.0,
                float(data[3]) if data[3] else 0.0,
                float(data[4]) if data[4] else 0.0,
                float(data[5]) if data[5] else 0.0,
                float(data[6]) if data[6] else 0.0,
                float(data[7]) if data[7] else 0.0,
                float(temp) if temp else 0.0,
                float(poP) if poP else 0.0,
                float(data[9]) if data[9] else 0.0,
                float(data[10]) if data[10] else 0.0,
                float(data[11]) if data[11] else 0.0,
            ]
            dataListv2.append(processed_data)
        except ValueError as e:
            print(f"Error processing data: {data}. Error: {e}")
            continue  
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
    maxValues = [100,1,1,1,1,1,1,1,1,1,1,1]
    for data in dataListv2:
        for i in range(12):
            data[i] = round(data[i] / maxValues[i], 4)
    return dataListv2



    


normalizer(getMaximums(dataRemake(fileRead('testRunV4.csv'))),  dataRemake(fileRead('testRunV4.csv')))

header = "Time of Scrape, Flight Zoning, MC, NC, LNC, SPOC, INTLC, Temperature, PoP, Month, Day of Week, Holiday"
dataList = fileRead('cleaned_output_file.csv')
dataListv2 = dataRemake(dataList)[1::]
maxValues = getMaximums(dataListv2)
normalizedData = normalizer(maxValues, dataListv2)
    
# Write the normalized data to a new CSV file
with open("NormalizedDataV1.csv", "w") as file:
    file.write(header + "\n")  # Write the header
    for data in normalizedData:
        file.write(",".join(map(str, data)) + "\n")
