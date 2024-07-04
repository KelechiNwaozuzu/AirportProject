import joblib
#import departureFilter


# Import necessary libraries
import joblib

# Define the predict function
def predict():
    # Load the pre-trained RandomForestRegressor model from a file
    rfr = joblib.load('forestRegressor_model.pkl')
    
    # Define the data point for prediction
    # The data point includes: time, flights zoning, temperature, chance of rain, month, and holiday status
    point_for_predic = [[20., 1600, 84, 0.0, 7.0, 3.0, 0.0]]
    
    # Use the loaded model to make a prediction for the given data point
    predict = rfr.predict(point_for_predic)
    
    # Print the prediction result
    print(predict)

# Call the predict function
predict()