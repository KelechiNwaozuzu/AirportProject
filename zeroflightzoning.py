import pandas as pd

def remove_zero_flight_zoning(input_csv, output_csv):
    # Step 1: Read the CSV file
    data = pd.read_csv(input_csv)
    
    # Step 2: Filter rows where 'Flight Zoning' is zero
    cleaned_data = data[data[' Flight Zoning'] != 0]
    
    # Step 3: Save the cleaned data to a new CSV file
    cleaned_data.to_csv(output_csv, index=False)

# Example usage
input_csv = 'testRunV4.csv'
output_csv = 'cleaned_output_file.csv'
remove_zero_flight_zoning(input_csv, output_csv)
