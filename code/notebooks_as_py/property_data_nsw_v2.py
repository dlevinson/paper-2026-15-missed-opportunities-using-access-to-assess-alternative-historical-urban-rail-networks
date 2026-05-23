# Exported from Property_data_NSW_V2.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1

import pandas as pd
import os

# Folder containing the CSV files
folder_path = "C:/Users/m1llz/Downloads/LV_20241101"

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
combined_df.to_csv('C:/Users/m1llz/Downloads/combined_valuation_file_v2.csv', index=False)

# Display the first few rows of the combined DataFrame
print(combined_df.head())

# %% Cell 2
csv_path = 'C:/Users/m1llz/Downloads/combined_valuation_file_v2.csv'
csv_data = pd.read_csv(csv_path)
csv_data

# %% Cell 3
csv_data['AREA'] = csv_data.apply(
    lambda row: row['AREA'] * 10000 if row['AREA TYPE'] == 'H' else row['AREA'],
    axis=1
)

csv_data

# %% Cell 4
import geopandas as gpd

shapefile_path = 'C:/Users/m1llz/Downloads/89459a8e-7107-47d8-bc10-475ff459176a/Property.shp'


    
gdf = gpd.read_file(shapefile_path)

# %% Cell 5
gdf

# %% Cell 6

shapefile_path1 = 'C:/Users/m1llz/Downloads/89459a8e-7107-47d8-bc10-475ff459176a/Property_1.shp'


    
gdf1 = gpd.read_file(shapefile_path1)
gdf1

# %% Cell 7
combined_gdf = pd.concat([gdf, gdf1], ignore_index=True)
combined_gdf

# %% Cell 8
merged_house = combined_gdf.merge(csv_data, left_on='propid', right_on='PROPERTY ID', how='inner')
merged_house

# %% Cell 9
gdf_cleaned = merged_house.drop_duplicates(subset=['propid'], keep='first')
gdf_cleaned

# %% Cell 10
print(gdf_cleaned.crs)
#print(merged_access.crs)

# %% Cell 11
gdf_reprojected = gdf_cleaned.to_crs("EPSG:3308")
gdf_reprojected

# %% Cell 12
columns_to_keep = ['propid', 'geometry',  'DISTRICT NAME', 'PROPERTY ID', 'AREA', 'AREA TYPE', 'BASE DATE 1', 'LAND VALUE 1']  # Replace with your actual column names
gdf_slimmed = gdf_reprojected[columns_to_keep]
gdf_slimmed

# %% Cell 13
output_path = 'C:/Users/m1llz/Downloads/NSW_house_all_data_v2.shp'
gdf_slimmed.to_file(output_path, driver='ESRI Shapefile')

# %% Cell 14

