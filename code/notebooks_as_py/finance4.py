# Exported from Finance4.ipynb. Outputs removed; execution order preserved where present.


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
csv_house_data.head()

# %% Cell 6
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

# %% Cell 7
csv_house_data['Sale history'] = csv_house_data['Sale history'].apply(convert_to_dict)

# %% Cell 8
csv_house_data

# %% Cell 9
def convert_to_dict(value):
    if pd.isna(value):  # Skip if the value is None or NaN
        return None
    
    if isinstance(value, dict):  # If it's already a dictionary, return it as is
        return value
    
    if isinstance(value, str):  # Only try to convert if it's a string
        try:
            # Convert the string representation of a dictionary to an actual dictionary
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return None  # Return None if the conversion fails
    
    return None  # Return None for any other types

# Apply the function to convert the strings to dictionaries
csv_house_data['Sale history'] = csv_house_data['Sale history'].apply(convert_to_dict)

csv_house_data

# %% Cell 10
print(csv_house_data.dtypes)

# %% Cell 11
csv_house_data['Sale history'] = csv_house_data['Sale history'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# %% Cell 12
def convert_to_float(amount_str):
    if 'M' in amount_str:
        return float(amount_str.replace('M', '').replace('$', '').replace(',', '').strip()) * 1_000_000
    elif 'k' in amount_str:
        return float(amount_str.replace('k', '').replace('$', '').replace(',', '').strip()) * 1_000
    else:
        return float(amount_str.replace('$', '').replace(',', '').strip())

# Function to extract the first 'Sold' date and amount
def extract_date_and_amount(sale_history):
    # Ensure sale_history is a dictionary (convert if needed)
    if isinstance(sale_history, str):
        try:
            sale_history = ast.literal_eval(sale_history)  # Convert string to dictionary
        except (ValueError, SyntaxError):
            return pd.Series([None, None])  # Return None if conversion fails

    # Check if sale_history is a valid dictionary
    if isinstance(sale_history, dict):
        for date, value in sale_history.items():
            # Check if the value starts with 'Sold'
            if "Sold" in value:
                # Ensure there is a dollar sign in the value before splitting
                if '$' in value:
                    amount_str = value.split('$')[1]  # Get the string after the '$'
                    try:
                        amount = convert_to_float(amount_str)  # Convert to float
                        return pd.Series([date, amount])  # Return date and amount as a Series
                    except ValueError:
                        return pd.Series([None, None])  # Return None if conversion fails
    return pd.Series([None, None])  # Return None if no 'Sold' entry is found

# %% Cell 13
csv_house_data[['Date Sold', 'Amount Sold']] = csv_house_data['Sale history'].apply(extract_date_and_amount)

# %% Cell 14
csv_house_data

# %% Cell 15
csv_house_data.iloc[3,16]

# %% Cell 16
csv_house_data2 = csv_house_data.dropna(subset=['Date Sold', 'Amount Sold'])
csv_house_data2

# %% Cell 17
csv_house_data2.head()

# %% Cell 18
import datetime

csv_house_data2['Date Sold'] = pd.to_datetime(csv_house_data2['Date Sold'], format='%d %b %Y', errors='coerce')

csv_house_data2

# %% Cell 19
csv_house_data3 = csv_house_data2[csv_house_data2['Longitude'] >= 150]
csv_house_data3

# %% Cell 20

start_date = '2015-01-01'
end_date = '2018-12-31'

# Filter the DataFrame based on the date range
csv_house_data3 = csv_house_data3[(csv_house_data3['Date Sold'] >= start_date) & (csv_house_data3['Date Sold'] <= end_date)]

csv_house_data3

# %% Cell 21
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


# Create a geometry column from latitude and longitude
geometry = [Point(lon, lat) for lon, lat in zip(csv_house_data3['Longitude'], csv_house_data3['Latitude'])]
real_estate_gdf = gpd.GeoDataFrame(csv_house_data3, geometry=geometry)

# Set the same coordinate reference system (CRS) for both GeoDataFrames
real_estate_gdf.set_crs(epsg=4283, inplace=True)  # Assuming WGS84 for lat/lon
#accessibility_gdf.set_crs(epsg=4326, inplace=True)  # Ensure the CRS matches

# %% Cell 22
shapefile_path1 = 'C:/Users/m1llz/Downloads/2016_SA1_shape/SA1_2016_AUST.dbf'



    
gdf_abs = gpd.read_file(shapefile_path1)

gdf_abs = gdf_abs[gdf_abs['STATE_NAME'] == 'New South Wales']
gdf_abs

# %% Cell 23
gdf_abs = gdf_abs.dropna(subset=['geometry'])
gdf_abs

# %% Cell 24
#gdf_projected2 = gdf_abs.to_crs(epsg=4283)
#gdf_projected2

# %% Cell 25
joined2 = gpd.sjoin(real_estate_gdf, gdf_abs, how='left', predicate='within')
joined2

# %% Cell 26
joined2 = joined2.dropna(subset=['SA1_7DIGIT'])
joined2

# %% Cell 27
csv_path_income = 'C:/Users/m1llz/Downloads/2016_GCP_SA1_for_NSW_short-header/2016 Census GCP Statistical Area 1 for NSW/2016Census_G02_NSW_SA1.csv'


csv_abs_data = pd.read_csv(csv_path_income)

csv_abs_data

# %% Cell 28
joined2['SA1_7DIGIT'] = joined2['SA1_7DIGIT'].astype(str)
csv_abs_data['SA1_7DIGIT'] = csv_abs_data['SA1_7DIGIT'].astype(str)

# %% Cell 29
merged_gdf = joined2.merge(csv_abs_data, on='SA1_7DIGIT')

merged_gdf

# %% Cell 30
gdf_projected = merged_gdf.to_crs(epsg=3308)
gdf_projected

# %% Cell 31
gdf_projected = gdf_projected.rename(columns={'index_right': 'right_index_col'})

# %% Cell 32
import geopandas as gpd

shapefile_path_30 = 'C:/Users/m1llz/Downloads/2016_access_45mins.shp'


    
gdf_30 = gpd.read_file(shapefile_path_30)
gdf_30

# %% Cell 33
gdf_30 = gdf_30.drop(columns=['id','num_opport']).rename(columns={'EMP_2016_y': '30_Mins'})
gdf_30

# %% Cell 34
joined = gpd.sjoin(gdf_projected, gdf_30, how='left', predicate='within')

joined

# %% Cell 35
joined1 = joined.dropna(subset=['index_right'])
joined1

# %% Cell 36
'''
from datetime import datetime

filtered_df['Date Sold'] = pd.to_datetime(filtered_df['Date Sold'])

# Function to get the access column based on the year of date_sold
# Function to get the access column based on the year of date_sold
def get_access_for_sale(row):
    year_sold = row['Date Sold'].year
    if str(year_sold) in filtered_df.columns:
        return row[str(year_sold)]
    else:
        return None  # Handle if the year doesn't match any access column

# Apply the function to create the new column
filtered_df['access_for_sale_year'] = filtered_df.apply(get_access_for_sale, axis=1)
filtered_df
'''

# %% Cell 37
filtered_df_house = joined[joined['Building Type'] == 'House']
filtered_df_house

# %% Cell 38
filtered_df_house['Bathrooms'] = pd.to_numeric(filtered_df_house['Bathrooms'], errors='coerce')
filtered_df_house['Bedrooms'] = pd.to_numeric(filtered_df_house['Bedrooms'], errors='coerce')
filtered_df_house['CarSpaces'] = pd.to_numeric(filtered_df_house['CarSpaces'], errors='coerce')

filtered_df_house['Bathrooms'] = filtered_df_house['Bathrooms'].fillna(0)
filtered_df_house['Bedrooms'] = filtered_df_house['Bedrooms'].fillna(0)
filtered_df_house['CarSpaces'] = filtered_df_house['CarSpaces'].fillna(0)
#filtered_df2['Floor Size'] = filtered_df2['Floor Size'].fillna(0)
#rfiltered_df2['Land Size'] = filtered_df2['Land Size'].fillna(0)
filtered_df_house

# %% Cell 39
filtered_df_house['Floor Size'] = filtered_df_house['Floor Size'].astype(str).str.replace('m2', '', regex=False)

# Convert to integers (handling non-numeric values)
filtered_df_house['Floor Size'] = pd.to_numeric(filtered_df_house['Floor Size'], errors='coerce').fillna(0).astype(int)


filtered_df_house['Land Size'] = filtered_df_house['Land Size'].astype(str).str.replace('m2', '', regex=False)

# Convert to integers (handling non-numeric values)
filtered_df_house['Land Size'] = pd.to_numeric(filtered_df_house['Land Size'], errors='coerce').fillna(0).astype(int)


#house_result['Land Size'] = house_result['Floor Size'].str.replace('m2', '', regex=False).astype(int)
#house_result= house_result[(house_result['Floor Size'] > 0)]
#house_result= house_result[(house_result['Land Size'] > 0)]
filtered_df_house

# %% Cell 40
filtered_df_house['Year Built'] = pd.to_numeric(filtered_df_house['Year Built'], errors='coerce')

filtered_df_house['Building Age'] =  2018 - filtered_df_house['Year Built']
filtered_df_house

# %% Cell 41
from datetime import datetime
base_date = datetime(2018, 12, 31)

filtered_df_house['Date Sold'] = pd.to_datetime(filtered_df_house['Date Sold'])

# Calculate the difference in years
filtered_df_house['YearsSinceSell'] = (filtered_df_house['Date Sold'] - base_date).dt.days / 365.25
filtered_df_house

# %% Cell 42
'''
filtered_df_house= filtered_df_house[(filtered_df_house['Building Age'] > 0)]
filtered_df_house= filtered_df_house[(filtered_df_house['YearsSinceSell'] > 0)]
filtered_df_house
'''

# %% Cell 43
filtered_df_house['Land Value per m2'] = filtered_df_house['Amount Sold'] / filtered_df_house['Land Size']
filtered_df_house

# %% Cell 44
print(filtered_df_house['SA4_Name16'].unique())

# %% Cell 45
filtered_df_house1 = filtered_df_house[(filtered_df_house['SA4_Name16'] == 'Sydney - City and Inner South') | (filtered_df_house['SA4_Name16'] == 'Sydney - Inner South West') |(filtered_df_house['SA4_Name16'] == 'Sydney - Inner West') |(filtered_df_house['SA4_Name16'] == 'Sydney - Eastern Suburbs') |(filtered_df_house['SA4_Name16'] == 'Sydney - North Sydney and Hornsby')]
filtered_df_house1

# %% Cell 46


# Step 1: Calculate Q1, Q3, and IQR
Q1 = filtered_df_house1['Land Value per m2'].quantile(0.25)
Q3 = filtered_df_house1['Land Value per m2'].quantile(0.75)
IQR = Q3 - Q1

# Step 2: Define the bounds for filtering
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Step 3: Filter the DataFrame to select rows within the IQR
filtered_df_house2 = filtered_df_house1[(filtered_df_house1['Land Value per m2'] >= lower_bound) & (filtered_df_house1['Land Value per m2'] <= upper_bound)]

filtered_df_house2

# %% Cell 47
'''
import numpy as np
from scipy.stats import median_abs_deviation
# Calculate the Modified Z-scores for column 'z'
mad = median_abs_deviation(filtered_df_house['Land Value per m2'])
median_z = filtered_df_house['Land Value per m2'].median()

filtered_df_house['z_modified_zscore'] = 0.6745 * (filtered_df_house['Land Value per m2'] - median_z) / mad

# Identify outliers (Modified Z-score greater than threshold, e.g., 3.5)
threshold = 1
outliers = filtered_df_house[filtered_df_house['z_modified_zscore'].abs() < threshold]

outliers
'''

# %% Cell 48
#filtered_df_house.to_csv("C:/Users/m1llz/Downloads/house_sale_regression.csv", index=False)

# %% Cell 49
'''
import numpy as np

# Sample DataFrame


# Calculate the natural logarithm of 'sale_price' and store it in a new column
df_with_dummies['ln_sale_price'] = np.log(df_with_dummies['adjusted_price'])

# Calculate the natural logarithm of 'other_value' and store it in a new column
df_with_dummies['ln_access_for_sale_year'] = np.log(df_with_dummies['access_for_sale_year'])
df_with_dummies['ln_Bedrooms'] = np.log(df_with_dummies['Bedrooms'])
df_with_dummies['ln_Bathrooms'] = np.log(df_with_dummies['Bathrooms'])
df_with_dummies['ln_CarSpaces'] = np.log(df_with_dummies['CarSpaces'])
df_with_dummies['ln_Median_age_persons'] = np.log(df_with_dummies['Median_age_persons'])
df_with_dummies['ln_Median_tot_hhd_inc_weekly'] = np.log(df_with_dummies['Median_tot_hhd_inc_weekly'])
df_with_dummies['ln_Building Age'] = np.log(df_with_dummies['Building Age'])
'''

# %% Cell 50
import numpy as np

# Check for NaN values
nan_check = X.isna().any()

# Check for inf values
inf_check = np.isinf(X).any()

print("NaN values:", nan_check)
print("Inf values:", inf_check)

# %% Cell 51
filtered_df_house2 = filtered_df_house2.dropna(subset=['Building Age', 'YearsSinceSell'])

# %% Cell 52
filtered_df_house2 #= filtered_df_house2.replace([np.inf, -np.inf], np.nan).dropna()

# %% Cell 53
import statsmodels.api as sm



Y = filtered_df_house2['Land Value per m2']

# Independent variables (X1, X2, X3)
X = filtered_df_house2[[ 'Bathrooms', 'CarSpaces',    'Median_age_persons', 'Median_tot_hhd_inc_weekly', '30_Mins', 'Building Age',	'YearsSinceSell' ]]
X1 = filtered_df_house2[[ 'Bedrooms', 'Bathrooms', 'CarSpaces',    'Median_age_persons', 'Median_tot_hhd_inc_weekly',   'Building Age', '30_Mins', 'Building Age',	'YearsSinceSell' ]]
X = sm.add_constant(X)

model = sm.OLS(Y, X)
results = model.fit()

# Show the summary
print(results.summary())

# %% Cell 54
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Step 3: Plot the distributions
for col in X1:
    plt.figure(figsize=(8, 6))
    sns.histplot(filtered_df_house2[col], kde=True)  # kde=True adds a kernel density estimate curve
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

# %% Cell 55

df_with_dummies = filtered_df_house2[(filtered_df_house2['Bathrooms'] > 0) & (filtered_df_house2['Bathrooms'] <4)]
df_with_dummies = filtered_df_house2[(filtered_df_house2['Bedrooms'] > 0) & (filtered_df_house2['Bathrooms'] <4)]
df_with_dummies = filtered_df_house2[(filtered_df_house2['CarSpaces'] >= 0) & (filtered_df_house2['CarSpaces'] <4)]
df_with_dummies = filtered_df_house2[(filtered_df_house2['Median_age_persons'] > 30) & (filtered_df_house2['Median_age_persons'] <40)]
df_with_dummies = filtered_df_house2[(filtered_df_house2['Median_tot_hhd_inc_weekly'] > 500) & (filtered_df_house2['Median_tot_hhd_inc_weekly'] <4000)]
df_with_dummies = filtered_df_house2[(filtered_df_house2['Building Age'] > 0) & (filtered_df_house2['Building Age'] <60)]
#df_with_dummies = filtered_df_house2[(filtered_df_house2['access_for_sale_year'] > 0) & (df_with_dummies['access_for_sale_year'] <75000)]
#df_with_dummies = df_with_dummies.dropna(subset=['adjusted_price','Bedrooms', 'Bathrooms', 'CarSpaces',    'Median_age_persons', 'Median_tot_hhd_inc_weekly',   'Building Age', 'access_for_sale_year','2016','2017','2018'])

#df_with_dummies2 = df_with_dummies2.drop('2016', axis=1)

df_with_dummies

# %% Cell 56
#df_with_dummies2.reset_index(drop=True, inplace=True)
#df_with_dummies2

# %% Cell 57
#print("Endog Index:", Y2.index)
#print("Exog Index:", X2.index)

# %% Cell 58
import statsmodels.api as sm



Y = df_with_dummies['Land Value per m2']

# Independent variables (X1, X2, X3)
X = df_with_dummies[[ 'Bedrooms', 'Bathrooms', 'CarSpaces',    'Median_age_persons', 'Median_tot_hhd_inc_weekly',   'Building Age', '30_Mins', 'Building Age',	'YearsSinceSell' ]]
X1 = df_with_dummies[[ 'Bedrooms', 'Bathrooms', 'CarSpaces',    'Median_age_persons', 'Median_tot_hhd_inc_weekly',   'Building Age', '30_Mins', 'Building Age',	'YearsSinceSell' ]]
X = sm.add_constant(X)

model = sm.OLS(Y, X)
results = model.fit()

# Show the summary
print(results.summary())

# %% Cell 59
import statsmodels.api as sm

#ln_sale_price	ln_access_for_sale_year	ln_Bedrooms	ln_Bathrooms	ln_CarSpaces	ln_Median_age_persons	ln_Median_tot_hhd_inc_weekly	ln_Building Age

Y = df_with_dummies['ln_sale_price']

# Independent variables (X1, X2, X3)
X = df_with_dummies[[ 'ln_Bathrooms',     'ln_Median_age_persons', 'ln_Median_tot_hhd_inc_weekly',   'Building Age', 'ln_access_for_sale_year','2017','2018']]
X1 = df_with_dummies[[ 'Bedrooms', 'Bathrooms', 'CarSpaces',    'Median_age_persons', 'Median_tot_hhd_inc_weekly',   'Building Age', 'access_for_sale_year','2016','2017','2018']]
X = sm.add_constant(X)

model = sm.OLS(Y, X)
results = model.fit()

# Show the summary
print(results.summary())

# %% Cell 60


# %% Cell 61


# %% Cell 62
print(df_with_dummies.dtypes)

# %% Cell 63
from statsmodels.stats.outliers_influence import variance_inflation_factor


vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# %% Cell 64
correlation_matrix = X.corr()
print(correlation_matrix)

# %% Cell 65

