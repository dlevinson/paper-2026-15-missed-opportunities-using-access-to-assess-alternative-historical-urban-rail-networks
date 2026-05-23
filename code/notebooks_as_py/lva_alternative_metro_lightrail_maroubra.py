# Exported from lva_alternative_metro_lightrail_maroubra.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import pandas as pd
import os


csv_path = 'C:/Users/m1llz/Downloads/combined_valuation_file.csv'
csv_data = pd.read_csv(csv_path)
csv_data

# %% Cell 2
csv_path1 = 'C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/Alternative Metro/With Maroubra/Alternative Metro Maroubra LVA_v2.csv'
csv_access = pd.read_csv(csv_path1)
csv_access

# %% Cell 3
csv_data.head()

# %% Cell 4
csv_data.iloc[1]

# %% Cell 5
csv_data['AREA'] = csv_data.apply(
    lambda row: row['AREA'] * 10000 if row['AREA TYPE'] == 'H' else row['AREA'],
    axis=1
)

csv_data

# %% Cell 6
import geopandas as gpd

shapefile_path = 'C:/Users/m1llz/Downloads/89459a8e-7107-47d8-bc10-475ff459176a/Property.shp'


    
gdf = gpd.read_file(shapefile_path)

# %% Cell 7
gdf

# %% Cell 8

shapefile_path1 = 'C:/Users/m1llz/Downloads/89459a8e-7107-47d8-bc10-475ff459176a/Property_1.shp'


    
gdf1 = gpd.read_file(shapefile_path1)
gdf1

# %% Cell 9
combined_gdf = pd.concat([gdf, gdf1], ignore_index=True)
combined_gdf

# %% Cell 10
merged_house = combined_gdf.merge(csv_data, left_on='propid', right_on='PROPERTY ID', how='inner')
merged_house

# %% Cell 11
gdf_cleaned = merged_house.drop_duplicates(subset=['propid'], keep='first')
gdf_cleaned

# %% Cell 12
import geopandas as gpd

shapefile_path2 = 'C:/Users/m1llz/Downloads/UNI FILES/tpa_spatial_tz_nsw_2016_shp/TZ_NSW_2016.dbf'



    
gdf_tz = gpd.read_file(shapefile_path2)

# %% Cell 13
gdf_tz

# %% Cell 14
merged_access = gdf_tz.merge(csv_access, left_on='TZ16_CODE', right_on='TZ16_CODE', how='inner')
merged_access

# %% Cell 15
print(gdf_cleaned.crs)
print(merged_access.crs)

# %% Cell 16
gdf_reprojected = gdf_cleaned.to_crs("EPSG:3308")
gdf_reprojected

# %% Cell 17
joined_access_and_house = gpd.sjoin(gdf_reprojected, merged_access, how='inner', predicate='within')
joined_access_and_house

# %% Cell 18
#joined_access_and_house = joined_access_and_house.drop(columns=['Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20'])
#joined_access_and_house

# %% Cell 19
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

# %% Cell 20
joined_access_and_house['30_log'] = joined_access_and_house['LAND VALUE 1']  * (joined_access_and_house['30 Mins']/ joined_access_and_house['Base 30 Mins']) * 0.2052
lva_30_log = joined_access_and_house['30_log'].sum()
print(lva_30_log)

joined_access_and_house['45_log'] = joined_access_and_house['LAND VALUE 1']  * (joined_access_and_house['45 Mins']/ joined_access_and_house['Base 45 Mins']) * 0.2229
lva_45_log = joined_access_and_house['45_log'].sum()
print(lva_45_log)

joined_access_and_house['60_log'] = joined_access_and_house['LAND VALUE 1']  * (joined_access_and_house['60 Mins']/ joined_access_and_house['Base 60 Mins']) * 0.2201
lva_60_log = joined_access_and_house['60_log'].sum()
print(lva_60_log)

# %% Cell 21

