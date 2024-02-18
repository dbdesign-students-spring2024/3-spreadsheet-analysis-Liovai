# Import pandas
import pandas as pd

file_path = 'data/Metal_Content_of_Consumer_Products_Tested_by_the_NYC_Health_Department_20240217.csv'
data = pd.read_csv(file_path)

# Munge the data
# 1. Remove the 'DELETED' column as no data stored in the column
cleaned_data = data.drop(columns=['DELETED'])

# 2. Drop rows with any missing values
cleaned_data = cleaned_data.dropna()

# 3. Add a new column indicating if concentration exceeds 5 ppm
cleaned_data['HIGH_CONCENTRATION'] = cleaned_data['CONCENTRATION'] > 5

# 4. Make 'COLLECTION_DATE' into standard date format
cleaned_data['COLLECTION_DATE'] = pd.to_datetime(cleaned_data['COLLECTION_DATE']).dt.date

# 5. Add a new column indicating if 'CONCENTRATION' is -1
cleaned_data['CONCENTRATION_IS_NEGATIVE_ONE'] = data['CONCENTRATION'] == -1

# 6. Unit conversion
def convert_to_ppm(value, unit):
    if unit == 'MG/L':
        return value  # 1 mg/L is approximately equal to 1 ppm for water (assumption)
    elif unit == 'MG/KG-DRY':
        return value  # equals to 1 ppm for solids
    elif unit == 'ppm':
        return value
    elif unit == 'MG/CM^2':
        # Need additional context, set None for now
        return None
    else:
        return None

# Apply conversion to a new column
cleaned_data['CONCENTRATION_PPM'] = cleaned_data.apply(lambda row: convert_to_ppm(row['CONCENTRATION'], row['UNITS']), axis=1)

# Define the path for the cleaned data file
output_file_path = 'data/clean_data.csv'  # Replace with the desired output file path

# Save the cleaned data
cleaned_data.to_csv(output_file_path, index=False)

