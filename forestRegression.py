from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import csv
import numpy as np
import matplotlib.pyplot as plt
import joblib




# Load data from CSV file
data = pd.read_csv("NormalizedDataV1.csv")


# Drop specific columns and split the data into features (x) and target variable (y)
columnsToDrop = [' MC', ' NC', ' LNC', ' SPOC', ' INTLC']
x = data.drop(columns = columnsToDrop)
#Iloc esseintially makes the data indexable
y = data.iloc[:, 2]
""""------------------------------------------------------"""

"""
#print("x: ")
#print(x)
#print("----------------------------")
#print("y: ")
#print(y)
"""

# Initialize the RandomForestRegressor model with a random state for reproducibility
rfr = RandomForestRegressor(random_state = 69)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2,random_state = 69)

# Train the model on the training data
rfr.fit(x_train, y_train)

# Make predictions on the test data
prediction = rfr.predict(x_test)

# Save the trained model to a file for future use
joblib.dump (rfr, 'forestRegressor_model.pkl')

# Evaluate the model using various metrics and print the results
print(mean_squared_error(y_test, prediction))
print(mean_absolute_error(y_test, prediction))
print(r2_score(y_test, prediction))


# Print predictions and ground truth values for comparison
print("prediction:")
print(prediction)
print("Ground Truth: {y_test}")
print(y_test)
#print(type(y_test))


# Convert y_test to a numpy array
y_test = y_test.to_numpy()
print(y_test)

""""------------------------------------------------------"""

# Save the predictions and ground truth values to a CSV file for further analysis
file = open("statsAnalysis.csv", "w", newline ='')
file.write("Ground Truth, Prediction\n")
for i in range(len(prediction)):
    file.write("{}, {}\n".format(y_test[i], prediction[i]))
file.close()

#RSCORE tracking as time progresses and more data is added! 
#RSCORE CURRENTLY: v07/01/2024 = .80, v07/03/2026 = .81,

""""------------------------------------------------------"""


# This code snippet performs several operations to visualize the relationship between
# the ground truth values and the squared errors of the predictions.

data = pd.read_csv("statsAnalysis.csv")
df = pd.DataFrame(data)
# Calculate errors
df['Error'] = df['Ground Truth'] - df[' Prediction']
df['Squared Error'] = np.square(df['Error'])
# Calculate the linear regression
slope, intercept = np.polyfit(df['Ground Truth'], df['Squared Error'], 1)
# Plot the scatter plot with vertical lines
plt.figure(figsize=(10, 6))
plt.scatter(df['Ground Truth'], df['Squared Error'], color='purple', label='Squared Error')
# Plot the regression line
x = np.linspace(min(df['Ground Truth']), max(df['Ground Truth']), 100)
y = slope * x + intercept
plt.plot(x, y, color='black', linestyle='-', linewidth=2, label='Regression Line')
# Titles and labels
plt.title('Ground Truth vs Squared Error')
plt.xlabel('Ground Truth')
plt.ylabel('Squared Error')
plt.legend()
plt.grid(True)
# Show plot
plt.show()

















