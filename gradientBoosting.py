import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
from datetime import datetime
print("Starting at:" + str(datetime.now()))
# Load data from CSV file
data = pd.read_csv("NormalizedDataV1.csv")

# Drop specific columns and split the data into features (x) and target variable (y)
columnsToDrop = [' MC', ' NC', ' LNC', ' SPOC', ' INTLC']
x = data.drop(columns=columnsToDrop)
y = data.iloc[:, 2]

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=69)

# Define the parameter grid for GridSearchCV
param_grid = {
    'n_estimators': [276, 278, 280, 282],
    'learning_rate': [0.149, 0.15, 0.151],
    'max_depth': [7, 8, 9],
    'min_samples_split': [5, 6, 7]
}

# Initialize GridSearchCV with GradientBoostingRegressor
grid_search = GridSearchCV(estimator=GradientBoostingRegressor(random_state=69),
                           param_grid=param_grid, cv=3, scoring='r2', n_jobs=-1)

# Fit GridSearchCV to the training data
grid_search.fit(x_train, y_train)

# Print the best parameters found by GridSearchCV
print("Best parameters found: ", grid_search.best_params_)

# Train the model with the best parameters
gbr = grid_search.best_estimator_
gbr.fit(x_train, y_train)

# Make predictions on the test data
prediction = gbr.predict(x_test)

# Save the trained model to a file for future use
joblib.dump(gbr, 'gradientBoostingRegressor_model.pkl')

# Evaluate the model using various metrics and print the results
print("Mean Squared Error: " + str(mean_squared_error(y_test, prediction)))
print("Mean Absolute Error: " + str(mean_absolute_error(y_test, prediction)))
print("R2 Score: " + str(r2_score(y_test, prediction)))

# Print predictions and ground truth values for comparison
print("Prediction:")
print(prediction) 
print("Ground Truth:")
print(y_test.to_numpy())



print("Ending at:" + str(datetime.now()))
with open("statsAnalysisGB.csv", "w", newline='') as file:
    file.write("Ground Truth, Prediction\n")
    for truth, pred in zip(y_test, prediction):
        file.write("{}, {}\n".format(truth, pred))
print("Analysis printing completed successfully.")

    


