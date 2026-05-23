# Exported from lva_lightrail_oxford_st.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import pandas as pd
import os


csv_path1 = 'C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/Lightrail/Oxford Street/Oxford Street LVA v2.csv'


csv_access = pd.read_csv(csv_path1)
csv_access

# %% Cell 2
import geopandas as gpd

shapefile_path2 = 'C:/Users/m1llz/Downloads/UNI FILES/tpa_spatial_tz_nsw_2016_shp/TZ_NSW_2016.dbf'



    
gdf_tz = gpd.read_file(shapefile_path2)

# %% Cell 3
gdf_tz

# %% Cell 4
merged_access = gdf_tz.merge(csv_access, left_on='TZ16_CODE', right_on='TZ16_CODE', how='inner')
merged_access

# %% Cell 5
import geopandas as gpd

shapefile_path = 'C:/Users/m1llz/Downloads/NSW_house_all_data_v2.shp'



    
gdf = gpd.read_file(shapefile_path)

# %% Cell 6
gdf

# %% Cell 7
joined_access_and_house = gpd.sjoin(gdf, merged_access, how='inner', predicate='within')
joined_access_and_house

# %% Cell 8
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

# %% Cell 9
joined_access_and_house['30_log'] = joined_access_and_house['LAND VALUE']  * (joined_access_and_house['30 Mins']/ joined_access_and_house['Base 30 Mins']) * 0.2052
lva_30_log = joined_access_and_house['30_log'].sum()
print(lva_30_log)

joined_access_and_house['45_log'] = joined_access_and_house['LAND VALUE']  * (joined_access_and_house['45 Mins']/ joined_access_and_house['Base 45 Mins']) * 0.2229
lva_45_log = joined_access_and_house['45_log'].sum()
print(lva_45_log)

joined_access_and_house['60_log'] = joined_access_and_house['LAND VALUE']  * (joined_access_and_house['60 Mins']/ joined_access_and_house['Base 60 Mins']) * 0.2201
lva_60_log = joined_access_and_house['60_log'].sum()
print(lva_60_log)

# %% Cell 10
aggregate = joined_access_and_house.groupby('TZ16_CODE')[['30_lin','45_lin','60_lin','30_log','45_log','60_log']].sum().reset_index()
aggregate['Average_Price'] = aggregate[['30_lin', '45_lin', '60_lin', '30_log', '45_lin','60_lin']].mean(axis=1)
aggregate.to_csv('C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/Lightrail/Oxford Street/TravelZone_Uplift.csv', index = False)
aggregate
