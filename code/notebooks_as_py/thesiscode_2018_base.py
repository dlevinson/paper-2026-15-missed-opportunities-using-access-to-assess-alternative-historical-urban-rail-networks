# Exported from THESISCODE 2018 Base.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import geopandas as gpd

shapefile_path = 'C:/Users/m1llz/Downloads/UNI FILES/tpa_spatial_tz_nsw_2016_shp/TZ_NSW_2016.dbf'



    
gdf = gpd.read_file(shapefile_path)

# %% Cell 2
gdf

# %% Cell 3
sorted_gdf=gdf.sort_values(by='TZ16_CODE', ascending = True)

sorted_gdf.to_file('sorted_TZ_NSW_2016.dbf')

sorted_gdf.reset_index(drop=True, inplace=True)

sorted_gdf

# %% Cell 4
import pandas as pd

csv_path = 'C:/Users/m1llz/Downloads/UNI FILES/tzp22-employment-by-tz-2016-2066.csv'
csv_job_data = pd.read_csv(csv_path)
csv_job_data

# %% Cell 5
csv_path1 = 'C:/Users/m1llz/Downloads/UNI FILES/tzp22-population-and-dwellings-erp_popd_pnpd_opd_spd-by-tz-2016-2066_0.csv'
csv_pop_data = pd.read_csv(csv_path1)
csv_pop_data

# %% Cell 6
#print(sorted_gdf.dtypes)
#print(csv_job_data.dtypes)

if sorted_gdf.iloc[50,0] == csv_job_data.iloc[50,0]:
    print('yay')
    print(sorted_gdf.iloc[50,0])
    print(csv_job_data.iloc[50,0])

else:
    print('oh no')

# %% Cell 7
common_column = 'TZ16_CODE'
columns_to_include =['SA2_Name16', 'SA3_Name16', 'SA4_Name16', 'LGA_Name18', 'EMP_2016'] 

# Ensure both have the same column names for the common identifier

#sorted_gdf.rename(columns={'TZ16_CODE': common_column}, inplace=True)
#csv_job_data.rename(columns={'TZ16_CODE': common_column}, inplace=True)



# Perform merge based on the common identifier and selected columns
merged_data = sorted_gdf.join(csv_job_data[columns_to_include])
merged_data

# %% Cell 8
merged_data1=merged_data.join(csv_pop_data['ERP_2016'])
merged_data1

# %% Cell 9
filtered_merge = merged_data1[merged_data1["SA4_Name16"].str.contains('Sydney')]
filtered_merge

# %% Cell 10
#filtered_merge.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/filtered_merge.csv", index=False)

# %% Cell 11



import matplotlib.pyplot as plt


filtered_gdf = merged_data[merged_data["SA4_Name16"].str.contains('Sydney')]

filtered_gdf


#filtered_gdf.plot()

#plt.show()

# %% Cell 12
shapefile_path_osm = 'C:/Users/m1llz/Downloads/UNI FILES/sydney-osm-withsydneymetrowest.osm.pbf'

#"C:\Users\m1llz\Downloads\UNI FILES\V2OSM-plswork.osm.pbf"
#"C:\Users\m1llz\Downloads\UNI FILES\UNISTUFF V2\full_greater_sydney_gtfs_static_0_editing.zip"
#"C:\Users\m1llz\Downloads\UNI FILES\UNISTUFF V2\full_greater_sydney_gtfs_static_0 (1).zip"

# %% Cell 13
filtered_gdf.explore()

# %% Cell 14
filtered_gdf.loc[:, 'id'] = filtered_gdf['TZ16_CODE'].copy()

# %% Cell 15
filtered_gdf

# %% Cell 16
filtered_gdf2 = filtered_gdf.to_crs('epsg:3308')
filtered_gdf2

# %% Cell 17
origins = filtered_gdf2.copy()
origins["geometry"] = origins.geometry.centroid
destinations = filtered_gdf2.copy()
destinations["geometry"] = destinations.geometry.centroid

# %% Cell 18
print(filtered_gdf2.loc[0])
print(filtered_gdf2.loc[2565])

# %% Cell 19
shapefile_path_gtfs1 = 'C:/Users/m1llz/Downloads/complete_gtfs_scheduled_data_20180928.zip'

# %% Cell 20
import r5py
import osmnx as ox

#G=ox.graph_from_file(shapefile_path_osm, simplify = False)

transport_network = r5py.TransportNetwork(
    shapefile_path_osm,
    [
        shapefile_path_gtfs1,
    ]
)

# %% Cell 21
import datetime


travel_time_matrix = r5py.TravelTimeMatrixComputer(
    transport_network,
    origins=origins,
    destinations=destinations,
    transport_modes=[r5py.TransportMode.TRANSIT, r5py.TransportMode.WALK],
    departure=datetime.datetime(2018, 9, 28, 8, 00, 00),
    departure_time_window=datetime.timedelta(hours=1),
    snap_to_network=True
).compute_travel_times()

# %% Cell 22
travel_time_matrix

# %% Cell 23
test_location = 146

travel_times_to_centre = travel_time_matrix[travel_time_matrix["to_id"] == test_location].copy()
travel_times_to_centre = travel_times_to_centre.set_index("from_id")[["travel_time"]]

grid_with_travel_time_to_centre = (
    filtered_gdf2.set_index("id").join(travel_times_to_centre)
)

grid_with_travel_time_to_centre

# %% Cell 24
grid_with_travel_time_to_centre.explore(
    column="travel_time",
    cmap="RdYlGn",
    tiles="CartoDB.Positron",
)

# %% Cell 25
median_travel_times = travel_time_matrix.groupby("from_id")["travel_time"].median()
median_travel_times

# %% Cell 26
grid_with_median_travel_times = (
    filtered_gdf2.set_index("id").join(median_travel_times)
)

grid_with_median_travel_times.explore(
    column="travel_time", 
    cmap="RdYlGn_r",
    tiles="CartoDB.Positron",
)

# %% Cell 27


merged_traveltime_matrix = pd.merge(travel_time_matrix, filtered_gdf2, left_on='to_id', right_on='TZ16_CODE', how='left')

merged_traveltime_matrix

# %% Cell 28
threshold =30
# Count the number of opportunities from each grid cell
opportunities = merged_traveltime_matrix.loc[merged_traveltime_matrix["travel_time"]<=threshold].groupby("from_id")["EMP_2016"].sum().reset_index()

# Rename the column for more intuitive one
opportunities = opportunities.rename(columns={"from_id": "num_opportunities"})

opportunities

# %% Cell 29
opportunities2 = filtered_gdf2.merge(opportunities, left_on="id", right_on="num_opportunities")
opportunities2

# %% Cell 30
opportunities2.to_csv("C:/Users/m1llz/Downloads/opportunities_v5.csv", index=False)

# %% Cell 31
import matplotlib.pyplot as plt

ax = opportunities2.plot(column="EMP_2016_y", figsize=(10,5), legend=True)
ax.set_title(f"Number of opportunities within {threshold} minutes."); 

plt.set_cmap('RdYlGn')
plt.show()
#plt.savefig('C:/Users/m1llz/Downloads/plot.jpg', format='jpg')

# %% Cell 32
opportunities2['APW'] =(opportunities2['EMP_2016_x'] * opportunities2['EMP_2016_y'])/opportunities2['EMP_2016_x'].sum()

#opportunities2
total_APW = opportunities2['APW'].sum()
print(total_APW)

# %% Cell 33


# %% Cell 34


# %% Cell 35

