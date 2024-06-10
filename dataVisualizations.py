import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D






#implementation and visuals for multiple regression model
# target: variables representing how you want data to be shown


"""
def buildData(fname, month = 6, dayOfWeek = 8):
    file = open(fname, "r")
    header  = file.readline()
    header = header.split(",")
    print(header[7])
    dataList = file.readlines()
    #print(dataList)
    file.close()

    data = {
        'Hour': [],
        '#ofZoning' : [],
        'MainCheckpoint' : []
    }

    for line in dataList:
        splitLine = line.strip().split(',')
        data['Hour'].append(int(splitLine[1][0:2]))
        data['#ofZoning'].append(int(splitLine[2]))
        data['MainCheckpoint'].append(int(splitLine[7]))
    #print(data)
    df = pd.DataFrame(data)


    return df
"""

def buildData(fname, month = 6, dayOfWeek = 8):
    file = open(fname, "r")
    header  = file.readline()
    header = header.split(",")
    print(header[3])
    dataList = file.readlines()
    #print(dataList)
    file.close()

    data = {
        'MC': [],
        'NC' : [],
        'LNC' : []
    }

    for line in dataList:
        splitLine = line.strip().split(',')
        data['MC'].append(int(splitLine[3]))
        data['NC'].append(int(splitLine[4]))
        data['LNC'].append(int(splitLine[5]))
    #print(data)
    df = pd.DataFrame(data)
    return df

def categorizeTheHours(time):
    if time >= 0 and time <= 59:
        return 0
    if time >= 100 and time < 159:
        return 1
    if time >= 200 and time < 259:
        return 2
    if time >= 300 and time < 359:
        return 3
    if time >= 400 and time < 459:
        return 4
    if time >= 500 and time < 559:
        return 5
    if time >= 600 and time < 659:
        return 6
    if time >= 700 and time < 759:
        return 7
    if time >= 800 and time < 859:
        return 8
    if time >= 900 and time < 959:
        return 9
    if time >= 1000 and time < 1059:
        return 10
    if time >= 1100 and time < 1159:
        return 11
    if time >= 1200 and time < 1259:
        return 12
    if time >= 1300 and time < 1359:
        return 13
    if time >= 1400 and time < 1459:
        return 14
    if time >= 1500 and time < 1559:
        return 15
    if time >= 1600 and time < 1659:
        return 16
    if time >= 1700 and time < 1759:
        return 17
    if time >= 1800 and time < 1859:
        return 18
    if time >= 1900 and time < 1959:
        return 19
    if time >= 2000 and time < 2059:
        return 20
    if time >= 2100 and time < 2159:
        return 21
    if time >= 2200 and time < 2259:
        return 22
    if time >= 2300 and time < 2359:
        return 23
    
    

def build3VarData(fname, xVar, yVar, zVar, categorizeHours):
    file = open(fname, "r")
    header  = file.readline()
    header = header.split(",")
    dataList = file.readlines()
    file.close()
    data = {
        xVar: [],
        yVar : [],
        zVar : []
    }

    for line in dataList:
        splitLine = line.strip().split(',')
        if xVar == 'Time of Scrape':
            if categorizeHours:
                data[xVar].append(categorizeTheHours(int((splitLine[header.index(" " + xVar)].replace(":", "")))))
            else:
                data[xVar].append(int((splitLine[header.index(" " + xVar)].replace(":", ""))))
        else:
            data[xVar].append(int(splitLine[header.index(" " + xVar)]))


        if yVar == 'Time of Scrape':
            if categorizeHours:
                data[yVar].append(categorizeTheHours(int((splitLine[header.index(" " + yVar)].replace(":", "")))))
            else:
                data[yVar].append(int((splitLine[header.index(" " + yVar)].replace(":", ""))))
        else:
            data[yVar].append(int(splitLine[header.index(" " + yVar)]))


        if zVar == 'Time of Scrape':
            if categorizeHours:
                data[zVar].append(categorizeTheHours(int((splitLine[header.index(" " + zVar)].replace(":", "")))))
            else:
                data[zVar].append(int((splitLine[header.index(" " + zVar)].replace(":", ""))))
        else:
            data[zVar].append(int(splitLine[header.index(" " + zVar)]))
    #print(data)
    df = pd.DataFrame(data)
    return df






def returnOLSRegression():
    """
    fname = input('Insert filename of data to read: ')
    df = buildData('testRunV4.csv')
    sns.pairplot(df)
    plt.show()
    """
    df = buildData('testRunV4.csv')
    X = df[['Hour', '#ofZoning']]
    y = df['MainCheckpoint']
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())

def runLinearRegression():
    df = buildData('testRunV4.csv')
    X = df[['Hour', '#ofZoning']]
    y = df['MainCheckpoint']
    reg = LinearRegression().fit(X, y)
    print("Intercept:", reg.intercept_)
    print("Coefficients:", reg.coef_)




def run3DVisualization(df):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['MC'], df['NC'], df['LNC'], color='blue', label='Actual Wait Time')

    ax.set_xlabel('Main CheckP')
    ax.set_ylabel('North CheckP')
    ax.set_zlabel('Lower North CheckP')
    ax.legend()
    plt.show()


def main():
    categorizeHours = False
    choiceModel = int(input('\n1) 3DVisualization\n2) OLS Regression\n3) Linear Regression\nSelect a Model/Visualization to run data on: '))
    resultMeaning = {
            1: 'Time of Scrape',
            2: 'Flight Zoning',
            3: 'MC',
            4: 'NC',
            5: 'LNC',
            6: 'SPOC',
            7: 'INTLC',
            8: 'Month',
            9: 'Day of Week',
            10: 'Holiday',
            'Y': True,
            'N': False
        }
    if choiceModel == 1:
        xVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect an X variable: (INDEPENDENT): '))]
        yVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Y variable: (INDEPENDENT): '))]
        zVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Z variable (DEPENDENT): '))]
        if xVar == 'Time of Scrape' or yVar == 'Time of Scrape' or zVar == 'Time of Scrape':
            categorizeHours = input("For the variable associated with 'Time of Scrape' would you like to categorize by hour? (Y/N): ").strip()
            categorizeHours = resultMeaning[categorizeHours]
    

        df = build3VarData('testRunV4.csv', xVar, yVar, zVar, categorizeHours)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df[xVar], df[yVar], df[zVar], color='blue', label='Actual Wait Time')

        ax.set_xlabel(xVar)
        ax.set_ylabel(yVar)
        ax.set_zlabel(zVar)
        ax.legend()
        plt.show()
    if choiceModel == 2:
        xVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect an X variable: (INDEPENDENT): '))]
        yVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Y variable: (INDEPENDENT): '))]
        zVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Z variable (DEPENDENT): '))]
        if xVar == 'Time of Scrape' or yVar == 'Time of Scrape' or zVar == 'Time of Scrape':
            categorizeHours = input("For the variable associated with 'Time of Scrape' would you like to categorize by hour? (Y/N): ").strip()
            categorizeHours = resultMeaning[categorizeHours]

        df = build3VarData('testRunV4.csv', xVar, yVar, zVar, categorizeHours)
        X = df[[xVar, yVar]]
        y = df[zVar]
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        print(model.summary())    

    if choiceModel == 3:
        xVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect an X variable: (INDEPENDENT): '))]
        yVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Y variable: (INDEPENDENT): '))]
        zVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Z variable (DEPENDENT): '))]
        print(xVar)
        if xVar == 'Time of Scrape' or yVar == 'Time of Scrape' or zVar == 'Time of Scrape':
            categorizeHours = input("For the variable associated with 'Time of Scrape' would you like to categorize by hour? (Y/N): ").strip()
            categorizeHours = resultMeaning[categorizeHours]

        df = build3VarData('testRunv4.csv', xVar, yVar, zVar, categorizeHours)
        X = df[['Hour', '#ofZoning']]
        y = df['MainCheckpoint']
        X = sm.add_constant(X)
            
        model = sm.OLS(y, X).fit()
        print(model.summary())
        
        

main()