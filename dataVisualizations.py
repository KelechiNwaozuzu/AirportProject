import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D

"""
Given a time, this method returns the hour that time falls on... 
- it basically just groups the time into an hour by hour period.
"""
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
    
    
"""
This HELPER function reads data from a CSV file, processes specified columns, and returns a pandas DataFrame containing the processed data. It is designed to handle a special case for the 'Time of Scrape' variable, where the hours can be categorized.

Parameters
fname (str): The name of the CSV file to read from.
xVar (str): The name of the first variable (column) to process.
yVar (str): The name of the second variable (column) to process.
zVar (str): The name of the third variable (column) to process.
categorizeHours (bool): A flag to indicate whether to categorize the 'Time of Scrape' hours.
"""
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
    print(data)
    df = pd.DataFrame(data)
    return df









    """
    The main function is the entry point of the program, which allows the user to choose between creating a 3D visualization or performing an OLS regression analysis. The function reads user inputs, processes data from a CSV file, and either generates a 3D scatter plot or performs an OLS regression based on the user's choice.

    Parameters
    This function does not take any parameters.
    Details
    User Choice: Prompts the user to choose between:

    1) 3DVisualization
    2) OLS Regression
    Variable Selection: Depending on the choice, the user is prompted to select variables for the analysis:

    X Variable (Independent)
    Y Variable (Independent)
    Z Variable (Dependent)
    Categorizing Hours: If the 'Time of Scrape' variable is chosen, the user can opt to categorize the hours.

    Data Processing: Calls the build3VarData function to read and process data from a CSV file based on the selected variables.

    3D Visualization:

    Creates a 3D scatter plot using the processed data.
    If 'Day of Week' is chosen as a variable, colors the scatter points based on the day.
    OLS Regression:

    Performs an OLS regression using the selected variables.
    Displays the regression summary.
    """


def main():
    categorizeHours = False
    choiceModel = int(input('\n1) 3DVisualization\n2) OLS Regression\n'))
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
        colors = {
        1: 'blue',
        2: 'red',
        3: 'green',
        4: 'orange',
        5: 'purple',
        6: 'brown',
        7: 'pink'
        }   
        xVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect an X variable: (INDEPENDENT): '))]
        yVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Y variable: (INDEPENDENT): '))]
        zVar = resultMeaning[int(input('\n1) Time of Scrape\n2) Flight Zoning\n3) Main Checkpoint\n4) North Checkpoint\n5) Lower North Checkpoint\n6) South Priorty Checkpoint\n7) International Checkpoint\n8) Month\n9) Day of Week\n10) Holiday\nSelect a Z variable (DEPENDENT): '))]
        if xVar == 'Time of Scrape' or yVar == 'Time of Scrape' or zVar == 'Time of Scrape':
            categorizeHours = input("For the variable associated with 'Time of Scrape' would you like to categorize by hour? (Y/N): ").strip()
            categorizeHours = resultMeaning[categorizeHours]
    

        df = build3VarData('testRunV4.csv', xVar, yVar, zVar, categorizeHours)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        if xVar == 'Day of Week' or yVar == 'Day of Week' or zVar == 'Day of Week':
            ax.scatter(df[xVar], df[yVar], df[zVar], color=df['Day of Week'].map(colors), label='Actual Wait Time')
        else:
            ax.scatter(df[xVar], df[yVar], df[zVar], color="Blue", label='Actual Wait Time')


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
        

main()