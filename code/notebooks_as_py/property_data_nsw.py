# Exported from Property_data_NSW.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1

import pandas as pd
import os
'''
# Folder containing the CSV files
folder_path = "C:/Users/m1llz/Downloads/LV_20241001 (1)"

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Initialize an empty list to hold the DataFrames
df_list = []

# Loop through the list of CSV files and append each one to the list
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    df_list.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
combined_df = pd.concat(df_list, ignore_index=True)

# Optionally, save the combined DataFrame to a new CSV file
combined_df.to_csv('C:/Users/m1llz/Downloads/combined_valuation_file.csv', index=False)

# Display the first few rows of the combined DataFrame
print(combined_df.head())
'''

# %% Cell 2
csv_path = 'C:/Users/m1llz/Downloads/combined_valuation_file.csv'
csv_data = pd.read_csv(csv_path)
csv_data

# %% Cell 3
import pandas as pd
from geopy.geocoders import Nominatim
import time

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Sample DataFrame
'''
data = {
    'Street Number': ['1600', '1', '350'],
    'Street Name': ['Amphitheatre Parkway', 'Infinite Loop', '5th Ave'],
    'Suburb': ['Mountain View', 'Cupertino', 'New York']
}
df = pd.DataFrame(data)
'''




# Function to combine address components into a full address
def create_full_address(row):
    return f"{row['HOUSE NUMBER']} {row['STREET NAME']}, {row['SUBURB NAME']}"

# Create a new column 'Full Address'
csv_data['Full Address'] = df.apply(create_full_address, axis=1)

# Function to geocode the full address
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        return pd.Series([None, None])

# Apply the geocode function to the 'Full Address' column
csv_data[['Latitude', 'Longitude']] = csv_data['Full Address'].apply(geocode_address)



# Display the updated DataFrame

# %% Cell 4
csv_data

# %% Cell 5
csv_path1 = 'C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/2001 Proposal/2001 LVAv2.csv'
csv_access = pd.read_csv(csv_path1)
csv_access

# %% Cell 6
csv_data.head()

# %% Cell 7
csv_data.iloc[1]

# %% Cell 8
csv_data['AREA'] = csv_data.apply(
    lambda row: row['AREA'] * 10000 if row['AREA TYPE'] == 'H' else row['AREA'],
    axis=1
)

csv_data

# %% Cell 9
df_grouped = csv_data.groupby("DISTRICT NAME")[["LAND VALUE 1", "AREA"]].sum().reset_index()

# Display the resulting DataFrame
df_grouped

# %% Cell 10
df_grouped.to_csv('C:/Users/m1llz/Downloads/grouped_data3.csv', index=False)

# %% Cell 11
csv_path2 = 'C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/2001 Proposal/2001 LVAv2.csv'
csv_jobs = pd.read_csv(csv_path2)
csv_jobs

# %% Cell 12
df_grouped1 = csv_jobs.groupby("SA2_Name16")[["Base 30 Mins", "30 Mins", "Base 45 Mins", "45 Mins", "Base 60 Mins", "60 Mins"]].sum().reset_index()

# Display the resulting DataFrame
df_grouped1

# %% Cell 13
matches = [
    {"SUBURB NAME": suburb, "SA2_Name16": sa2, "SA2_NAME16": row["SA2_NAME16"]}
    for suburb in df_grouped["SUBURB NAME"]
    for _, row in df_grouped1.iterrows()
    for sa2 in [row["SA2_Name16"]]
    if suburb in sa2  # Check if suburb name is contained in the SA2 name
]

# Convert matches into a DataFrame
matches_df = pd.DataFrame(matches)

# Merge the result back with the original df_grouped
#result_df = df_grouped.merge(matches_df, left_on="SUBURB NAME", right_on="SUBURB NAME", how="left")

#result_df

# %% Cell 14
matches_df

# %% Cell 15
df_expanded = df_grouped1.assign(SA2_Name16=df_grouped1['SA2_Name16'].str.split(' - ')).explode('SA2_Name16')

# Resetting the index (optional)
df_expanded.reset_index(drop=True, inplace=True)
df_expanded

# %% Cell 16
df_expanded.rename(columns={'SA2_Name16': 'SUBURB NAME'}, inplace=True)
df_expanded

# %% Cell 17
df_expanded['SUBURB NAME'] = df_expanded['SUBURB NAME'].str.upper()
df_expanded

# %% Cell 18
result_df = pd.merge(df_grouped, df_expanded, left_on='SUBURB NAME', right_on='SUBURB NAME', how='inner')
result_df

# %% Cell 19
import numpy as np


result_df['30_lin'] = result_df['AREA'] * result_df['30 Mins'] * 0.0325
lva  = result_df['30_lin'].sum()
print(lva)

# %% Cell 20
result_df['45_log'] = result_df['LAND VALUE 1'] * (result_df['45 Mins'] / result_df['Base 45 Mins'] ) * 0.2229
lva2 = result_df['45_log'].sum()
print(lva2)

# %% Cell 21
import geopandas as gpd

shapefile_path = 'C:/Users/m1llz/Downloads/89459a8e-7107-47d8-bc10-475ff459176a/Property.shp'


    
gdf = gpd.read_file(shapefile_path)

# %% Cell 22
gdf

# %% Cell 23

shapefile_path1 = 'C:/Users/m1llz/Downloads/89459a8e-7107-47d8-bc10-475ff459176a/Property_1.shp'


    
gdf1 = gpd.read_file(shapefile_path1)
gdf1

# %% Cell 24
combined_gdf = pd.concat([gdf, gdf1], ignore_index=True)
combined_gdf

# %% Cell 25
merged_house = combined_gdf.merge(csv_data, left_on='propid', right_on='PROPERTY ID', how='inner')
merged_house

# %% Cell 26
gdf_cleaned = merged_house.drop_duplicates(subset=['propid'], keep='first')
gdf_cleaned

# %% Cell 27
import geopandas as gpd

shapefile_path2 = 'C:/Users/m1llz/Downloads/UNI FILES/tpa_spatial_tz_nsw_2016_shp/TZ_NSW_2016.dbf'



    
gdf_tz = gpd.read_file(shapefile_path2)

# %% Cell 28
gdf_tz

# %% Cell 29
merged_access = gdf_tz.merge(csv_jobs, left_on='TZ16_CODE', right_on='TZ16_CODE', how='inner')
merged_access

# %% Cell 30
print(gdf_cleaned.crs)
print(merged_access.crs)

# %% Cell 31
gdf_reprojected = gdf_cleaned.to_crs("EPSG:3308")
gdf_reprojected

# %% Cell 32
joined_access_and_house = gpd.sjoin(gdf_reprojected, merged_access, how='inner', predicate='within')
joined_access_and_house

# %% Cell 33
joined_access_and_house = joined_access_and_house.drop(columns=['Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20'])
joined_access_and_house

# %% Cell 34
import numpy as np


joined_access_and_house['30_lin'] = joined_access_and_house['AREA']  * joined_access_and_house['30 Mins'] * 0.0325
lva_30_lin = joined_access_and_house['30_lin'].sum()
print(lva_30_lin)


joined_access_and_house['45_lin'] = joined_access_and_house['AREA']  * joined_access_and_house['45 Mins'] * 0.0109
lva_45_lin = joined_access_and_house['45_lin'].sum()
print(lva_45_lin)


joined_access_and_house['60_lin'] = joined_access_and_house['AREA']  * joined_access_and_house['60 Mins'] * 0.0051
lva_60_lin = joined_access_and_house['60_lin'].sum()
print(lva_60_lin)

# %% Cell 35
joined_access_and_house['30_log'] = joined_access_and_house['LAND VALUE 1']  * (joined_access_and_house['30 Mins']/ joined_access_and_house['Base 30 Mins']) * 0.2052
lva_30_log = joined_access_and_house['30_log'].sum()
print(lva_30_log)

joined_access_and_house['45_log'] = joined_access_and_house['LAND VALUE 1']  * (joined_access_and_house['45 Mins']/ joined_access_and_house['Base 45 Mins']) * 0.2229
lva_45_log = joined_access_and_house['45_log'].sum()
print(lva_45_log)

joined_access_and_house['60_log'] = joined_access_and_house['LAND VALUE 1']  * (joined_access_and_house['60 Mins']/ joined_access_and_house['Base 60 Mins']) * 0.2201
lva_60_log = joined_access_and_house['60_log'].sum()
print(lva_60_log)

# %% Cell 36
table = [
    {"Name": "Alice", "Age": 25, "City": "New York"},
    {"Name": "Bob", "Age": 30, "City": "Los Angeles"},
    {"Name": "Charlie", "Age": 35, "City": "Chicago"},
]

# Accessing data
for row in table:
    print(row["Name"], row["Age"], row["City"])
