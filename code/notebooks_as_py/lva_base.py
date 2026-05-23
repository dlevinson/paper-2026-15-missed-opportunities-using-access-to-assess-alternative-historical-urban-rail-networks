# Exported from lva_base.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import pandas as pd
import os


csv_path1 = 'C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/Base Case Data/base LVAv2.csv'


csv_access = pd.read_csv(csv_path1)
csv_access

# %% Cell 2
csv_path = 'C:/Users/m1llz/Downloads/UNI FILES/tzp22-employment-by-tz-2016-2066.csv'
csv_job_data = pd.read_csv(csv_path)
csv_job_data

# %% Cell 3
csv_joined = pd.merge(csv_access, csv_job_data, on = 'TZ16_CODE', how='inner')

csv_joined

# %% Cell 4
import numpy as np
list = csv_joined['SA3_Name16'].unique()

weighted_list_30 = []
weighted_list_45 = []
weighted_list_60 = []

for sa4 in list:
    csv_joined_sa4 = csv_joined[csv_joined['SA3_Name16'] == sa4]

    
    csv_joined_sa4['30_weighted_access'] = (csv_joined_sa4['Base 30 Mins'] * csv_joined_sa4['ERP_2016']) / csv_joined_sa4['ERP_2016'].sum()
    weighted_value_30 = csv_joined_sa4['30_weighted_access'].sum()
    weighted_list_30.append(weighted_value_30)


    csv_joined_sa4['45_weighted_access'] = (csv_joined_sa4['Base 45 Mins'] * csv_joined_sa4['ERP_2016']) / csv_joined_sa4['ERP_2016'].sum()
    weighted_value_45 = csv_joined_sa4['45_weighted_access'].sum()
    weighted_list_45.append(weighted_value_45)


    csv_joined_sa4['60_weighted_access'] = (csv_joined_sa4['Base 60 Mins'] * csv_joined_sa4['ERP_2016']) / csv_joined_sa4['ERP_2016'].sum()
    weighted_value_60 = csv_joined_sa4['60_weighted_access'].sum()
    weighted_list_60.append(weighted_value_60)


print(weighted_list_30)
print(weighted_list_45)
print(weighted_list_60)

# %% Cell 5
df = pd.DataFrame({
    'SA3': list,
    'PWA_30': weighted_list_30,
    'PWA_45': weighted_list_45,
    'PWA_60': weighted_list_60
})

df

# %% Cell 6
df['average'] = df[['PWA_30', 'PWA_45', 'PWA_60']].mean(axis=1)
df

# %% Cell 7
df_sorted = df.sort_values(by='average', ascending=False).reset_index(drop=True)
df_sorted

# %% Cell 8
df_sorted.to_csv("C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/Base Case Data/sa3_access.csv", index=False)

# %% Cell 9
import geopandas as gpd

shapefile_path2 = 'C:/Users/m1llz/Downloads/UNI FILES/tpa_spatial_tz_nsw_2016_shp/TZ_NSW_2016.dbf'



    
gdf_tz = gpd.read_file(shapefile_path2)

# %% Cell 10
gdf_tz

# %% Cell 11
merged_access = gdf_tz.merge(csv_access, left_on='TZ16_CODE', right_on='TZ16_CODE', how='inner')
merged_access

# %% Cell 12
import geopandas as gpd

shapefile_path = 'C:/Users/m1llz/Downloads/NSW_house_all_data_v2.shp'



    
gdf = gpd.read_file(shapefile_path)

# %% Cell 13
gdf

# %% Cell 14
joined_access_and_house = gpd.sjoin(gdf, merged_access, how='inner', predicate='within')
joined_access_and_house

# %% Cell 15
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

# %% Cell 16
joined_access_and_house['30_log'] = joined_access_and_house['LAND VALUE']  * (joined_access_and_house['30 Mins']/ joined_access_and_house['Base 30 Mins']) * 0.2052
lva_30_log = joined_access_and_house['30_log'].sum()
print(lva_30_log)

joined_access_and_house['45_log'] = joined_access_and_house['LAND VALUE']  * (joined_access_and_house['45 Mins']/ joined_access_and_house['Base 45 Mins']) * 0.2229
lva_45_log = joined_access_and_house['45_log'].sum()
print(lva_45_log)

joined_access_and_house['60_log'] = joined_access_and_house['LAND VALUE']  * (joined_access_and_house['60 Mins']/ joined_access_and_house['Base 60 Mins']) * 0.2201
lva_60_log = joined_access_and_house['60_log'].sum()
print(lva_60_log)

# %% Cell 17
aggregate = joined_access_and_house.groupby('TZ16_CODE')[['30_lin','45_lin','60_lin','30_log','45_log','60_log']].sum().reset_index()
aggregate['Average_Price'] = aggregate[['30_lin', '45_lin', '60_lin', '30_log', '45_lin','60_lin']].mean(axis=1)
aggregate.to_csv('C:/Users/m1llz/Documents/University/Year 5/Sem 2/Thesis/2001 Proposal/TravelZone_Uplift.csv', index = False)
aggregate

# %% Cell 18

