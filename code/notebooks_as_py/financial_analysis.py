# Exported from Financial_Analysis.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import pandas as pd

csv_path = 'C:/Users/m1llz/Downloads/RealEstateData_OnTheHouse/RealEstateData_OnTheHouse.csv'
csv_house_data = pd.read_csv(csv_path)
csv_house_data

# %% Cell 2
import ast

csv_house_data['Info(Labels:Values)'] = csv_house_data['Info(Labels:Values)'].apply(lambda x: ast.literal_eval(x))

# Expand the dictionary into separate columns
csv_house_data1 = pd.json_normalize(csv_house_data['Info(Labels:Values)'])
csv_house_data1

# %% Cell 3
csv_house_data = pd.concat([csv_house_data[['Region']],csv_house_data[['Address']],csv_house_data[['Latitude']],csv_house_data[['Longitude']],csv_house_data[['Bathrooms']],csv_house_data[['Bedrooms']],csv_house_data[['CarSpaces']], csv_house_data[['Info(Labels:Values)']], csv_house_data1, csv_house_data[['Listing type']],csv_house_data[['Sale history']],csv_house_data[['Postcode']]], axis=1)



csv_house_data

# %% Cell 4
csv_house_data = csv_house_data.drop(columns=['Info(Labels:Values)'])
csv_house_data

# %% Cell 5
import re

def convert_to_dict(value):
    # Check if it's a dictionary-like string
    if value.startswith("{"):
        # Clean and return as-is (no conversion needed)
        return value
    elif value.startswith("["):
        # Handle list-like string format
        match = re.match(r"\['([^']+) - (Sold .+)'\]", value)
        if match:
            date, sale_info = match.groups()
            return f"{{'{date}': '{sale_info}'}}"  # Return dictionary-like string
    return None

# %% Cell 6
csv_house_data['Sale history'] = csv_house_data['Sale history'].apply(convert_to_dict)

# %% Cell 7
csv_house_data

# %% Cell 8
def convert_to_dict(value):
    if pd.isna(value):  # Skip if the value is None or NaN
        return None
    try:
        # Convert the string representation of a dictionary to an actual dictionary
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None  # Return None if the conversion fails

# Apply the function to convert the strings to dictionaries
csv_house_data['Sale history'] = csv_house_data['Sale history'].apply(convert_to_dict)

csv_house_data

# %% Cell 9
csv_house_data.to_csv("C:/Users/m1llz/Downloads/edited_real_estate_data.csv", index=False)

# %% Cell 10
import pandas as pd

csv_path1 = 'C:/Users/m1llz/Downloads/edited_real_estate_data.csv'
csv1_house_data = pd.read_csv(csv_path1)
csv1_house_data

# %% Cell 11
value = csv1_house_data.loc[2, 'Sale history']  # Accessing value at row index 5 and column 'Sale history'
print(value)

# %% Cell 12
print(csv1_house_data['Sale history'].dtype)

# %% Cell 13
csv1_house_data['Sale history'] = csv1_house_data['Sale history'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# %% Cell 14
# Function to convert sale amount to float
def convert_to_float(amount_str):
    if 'M' in amount_str:
        return float(amount_str.replace('M', '').replace('$', '').replace(',', '').strip()) * 1_000_000
    elif 'K' in amount_str:
        return float(amount_str.replace('K', '').replace('$', '').replace(',', '').strip()) * 1_000
    else:
        return float(amount_str.replace('$', '').replace(',', '').strip())

# Function to extract date and amount sold
def extract_date_and_amount(sale_history):
    if isinstance(sale_history, dict) and len(sale_history) == 1:
        for date, value in sale_history.items():
            # Check if the value starts with 'Sold'
            if value.startswith('Sold'):
                # Ensure there is a dollar sign in the value before splitting
                if '$' in value:
                    amount_str = value.split('$')[1]  # Get the string after the '$'
                    try:
                        amount = convert_to_float(amount_str)  # Convert to float
                        return pd.Series([date, amount])  # Return date and amount as a Series
                    except ValueError:
                        return pd.Series([None, None])  # Return None if conversion fails
    return pd.Series([None, None])  # Return None if the format is incorrect

# %% Cell 15
csv1_house_data[['Date Sold', 'Amount Sold']] = csv1_house_data['Sale history'].apply(extract_date_and_amount)

# %% Cell 16
csv1_house_data

# %% Cell 17
csv1_house_data2 = csv1_house_data.dropna(subset=['Date Sold', 'Amount Sold'])
csv1_house_data2

# %% Cell 18
import datetime

csv1_house_data2['Date Sold'] = pd.to_datetime(csv1_house_data2['Date Sold'], format='%d %b %Y', errors='coerce')

csv1_house_data2

# %% Cell 19
test_data = csv1_house_data2[csv1_house_data2['Longitude'] >= 150]
test_data

# %% Cell 20
start_date = '2014-01-01'
end_date = '2019-12-31'

# Filter the DataFrame based on the date range
csv1_house_data3 = csv1_house_data2[(csv1_house_data2['Date Sold'] >= start_date) & (csv1_house_data2['Date Sold'] <= end_date)]

csv1_house_data3

# %% Cell 21
csv1_house_data3 = csv1_house_data3.dropna(subset=['Floor Size', 'Land Size'])
#csv1_house_data3


#csv1_house_data3['Floor Size'] = csv1_house_data3['Floor Size'].str.replace('m2', '', regex=False).astype(int)
csv1_house_data3 = csv1_house_data3[(csv1_house_data3['Floor Size'] > 0)]
csv1_house_data3

# %% Cell 22
csv1_house_data3['Region'] = csv1_house_data3['Region'].str.split().str[0].str.strip()

# Display the updated DataFrame
csv1_house_data3

# %% Cell 23
csv_path3 = 'C:/Users/m1llz/Downloads/average_opportunities_30.csv'
csv_jobs_30 = pd.read_csv(csv_path3)
csv_jobs_30

# %% Cell 24
expanded_rows = []

# Iterate through each row in the original DataFrame
for _, row in csv_jobs_30.iterrows():
    # Split the grouped suburbs by the separator ' - '
    suburbs = row['SA2_Name16'].split(' - ')
    
    # Append each suburb with the corresponding value to the new rows list
    for suburb in suburbs:
        expanded_rows.append({'SA2_Name16': suburb.strip(), 'Average Jobs Accessible': row['Average Jobs Accessible']})

# Convert the list of new rows to a DataFrame
expanded_df = pd.DataFrame(expanded_rows)
expanded_df

# %% Cell 25
expanded_df.rename(columns={'SA2_Name16': 'Region'}, inplace=True)
expanded_df

# %% Cell 26
expanded_df.to_csv("C:/Users/m1llz/Downloads/expanded_df.csv", index=False)

# %% Cell 27
csv_path4 = 'C:/Users/m1llz/Downloads/expanded_df.csv'
csv1_jobs_30 = pd.read_csv(csv_path4)
csv1_jobs_30

# %% Cell 28
result_inner = pd.merge(csv1_house_data3, csv1_jobs_30, on='Region', how='inner')

result_inner

# %% Cell 29
result_inner.tail()

# %% Cell 30
#result_inner.to_csv("C:/Users/m1llz/Downloads/edited_results_inner.csv", index=False)

# %% Cell 31
#csv1_house_data3.to_csv("C:/Users/m1llz/Downloads/edited_real_estate_data_v2.csv", index=False)

# %% Cell 32
csv_path4 = 'C:/Users/m1llz/Downloads/average_opportunities_45.csv'
csv_jobs_45 = pd.read_csv(csv_path4)
csv_jobs_45

# %% Cell 33
expanded_rows1 = []

# Iterate through each row in the original DataFrame
for _, row in csv_jobs_45.iterrows():
    # Split the grouped suburbs by the separator ' - '
    suburbs1 = row['SA2_Name16'].split(' - ')
    
    # Append each suburb with the corresponding value to the new rows list
    for suburb in suburbs1:
        expanded_rows1.append({'SA2_Name16': suburb.strip(), 'Average Jobs Accessible': row['Average Jobs Accessible']})

# Convert the list of new rows to a DataFrame
expanded_df1 = pd.DataFrame(expanded_rows1)
expanded_df1

# %% Cell 34
expanded_df1.to_csv("C:/Users/m1llz/Downloads/expanded_df1.csv", index=False)

# %% Cell 35
csv_path5 = 'C:/Users/m1llz/Downloads/expanded_df1.csv'
expanded_df1 = pd.read_csv(csv_path5)
expanded_df1

# %% Cell 36
result_inner1 = pd.merge(result_inner, expanded_df1, on='Region', how='inner')

result_inner1

# %% Cell 37
csv_path6 = 'C:/Users/m1llz/Downloads/average_opportunities_60.csv'
csv_jobs_60 = pd.read_csv(csv_path6)
csv_jobs_60

# %% Cell 38
expanded_rows2 = []

# Iterate through each row in the original DataFrame
for _, row in csv_jobs_60.iterrows():
    # Split the grouped suburbs by the separator ' - '
    suburbs2 = row['SA2_Name16'].split(' - ')
    
    # Append each suburb with the corresponding value to the new rows list
    for suburb in suburbs2:
        expanded_rows2.append({'SA2_Name16': suburb.strip(), 'Average Jobs Accessible': row['Average Jobs Accessible']})

# Convert the list of new rows to a DataFrame
expanded_df2 = pd.DataFrame(expanded_rows2)
expanded_df2

# %% Cell 39
expanded_df2.to_csv("C:/Users/m1llz/Downloads/expanded_df2.csv", index=False)

# %% Cell 40
csv_path7 = 'C:/Users/m1llz/Downloads/expanded_df2.csv'
expanded_df2 = pd.read_csv(csv_path7)
expanded_df2

# %% Cell 41
result_inner2 = pd.merge(result_inner1, expanded_df2, on='Region', how='inner')

result_inner2

# %% Cell 42
csv_path8 = 'C:/Users/m1llz/Downloads/median_income_sa2.csv'
csv_income = pd.read_csv(csv_path8)
csv_income

# %% Cell 43
expanded_rows_income = []

# Iterate through each row in the original DataFrame
for _, row in csv_income.iterrows():
    # Split the grouped suburbs by the separator ' - '
    suburbs_income = row['Region'].split(' - ')
    
    # Append each suburb with the corresponding value to the new rows list
    for suburb in suburbs_income:
        expanded_rows_income.append({'Region': suburb.strip(), 'Median Weekly Income': row['Median Weekly Income']})

# Convert the list of new rows to a DataFrame
expanded_df_income = pd.DataFrame(expanded_rows_income)
expanded_df_income

# %% Cell 44
#expanded_df_income.to_csv("C:/Users/m1llz/Downloads/expanded_df_income_v2.csv", index=False)

# %% Cell 45
test_output = csv1_house_data3[csv1_house_data3['Region']=='Woolooware']
test_output

# %% Cell 46
csv_path9 = 'C:/Users/m1llz/Downloads/expanded_df_income_v2.csv'
csv_income_df = pd.read_csv(csv_path9)
csv_income_df

# %% Cell 47
result_inner3 = pd.merge(result_inner2, csv_income_df, on='Region', how='inner')

result_inner3

# %% Cell 48
#result_inner3.to_csv("C:/Users/m1llz/Downloads/sorted_real_estate_data.csv", index=False)

# %% Cell 49
import statsmodels.api as sm

# %% Cell 50
result_inner3['Bathrooms'] = pd.to_numeric(result_inner3['Bathrooms'], errors='coerce')
result_inner3['Bedrooms'] = pd.to_numeric(result_inner3['Bedrooms'], errors='coerce')
result_inner3['CarSpaces'] = pd.to_numeric(result_inner3['CarSpaces'], errors='coerce')
result_inner3['Land Size'] = pd.to_numeric(result_inner3['Land Size'], errors='coerce')
#result_inner3['Median Weekly Income'] = pd.to_numeric(result_inner3['Median Weekly Income'], errors='coerce')

# %% Cell 51
result_inner3['Bathrooms'] = result_inner3['Bathrooms'].fillna(0)
result_inner3['Bedrooms'] = result_inner3['Bedrooms'].fillna(0)
result_inner3['CarSpaces'] = result_inner3['CarSpaces'].fillna(0)
result_inner3['Floor Size'] = result_inner3['Floor Size'].fillna(0)
result_inner3['Land Size'] = result_inner3['Land Size'].fillna(0)
result_inner3

# %% Cell 52
result_inner_filtered = result_inner3['Amount Sold'].dropna()
result_inner_filtered

# %% Cell 53
import numpy as np


column_to_check = 'Amount Sold'

# Step 2: Create a condition for filtering
condition = result_inner3[column_to_check].notna() & ~result_inner3[column_to_check].isin([np.inf, -np.inf])

# Step 3: Filter the DataFrame to remove rows with NaN or inf
filtered_result_inner3 = result_inner3[condition]

filtered_result_inner3

# %% Cell 54
print("NaN values:\n", result_inner3['Amount Sold'].isnull().sum())   # NaNs per column
print("Inf values:\n", np.isinf(result_inner3['Amount Sold']).sum())  # Inf per column

print(result_inner3['Amount Sold'].dtypes)

# %% Cell 55
house_result_inner3 = result_inner3[result_inner3['Building Type'] == 'House']
house_result_inner3

# %% Cell 56
# Step 1: Calculate Q1, Q3, and IQR
Q1 = house_result_inner3['Amount Sold'].quantile(0.25)
Q3 = house_result_inner3['Amount Sold'].quantile(0.75)
IQR = Q3 - Q1

# Step 2: Define the bounds for filtering
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Step 3: Filter the DataFrame to select rows within the IQR
filtered_house = house_result_inner3[(house_result_inner3['Amount Sold'] >= lower_bound) & (house_result_inner3['Amount Sold'] <= upper_bound)]

filtered_house

# %% Cell 57
Y = filtered_house['Amount Sold']

# Independent variables (X1, X2, X3)
X = filtered_house[['Bathrooms', 'Bedrooms', 'CarSpaces', 'Floor Size',  '45 Mins','Median Weekly Income']]

X = sm.add_constant(X)

model = sm.OLS(Y, X)
results = model.fit()

# Show the summary
print(results.summary())

# %% Cell 58
correlation_matrix = X.corrwith(Y)
print(correlation_matrix)

# %% Cell 59
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF for each column in exog
vif = pd.DataFrame()
vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["Variable"] = X.columns

print(vif)

# %% Cell 60
correlation_matrix = X.corr()
print(correlation_matrix)

# %% Cell 61
print(result_inner3.dtypes)

# %% Cell 62

