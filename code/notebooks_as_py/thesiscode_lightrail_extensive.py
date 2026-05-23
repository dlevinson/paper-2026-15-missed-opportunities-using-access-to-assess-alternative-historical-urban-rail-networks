# Exported from THESISCODE Lightrail-extensive.ipynb. Outputs removed; execution order preserved where present.


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
trips_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/trips.txt'
trips_txt_data = pd.read_csv(trips_txt_path)
#trips_txt_data
#filtered_trips_txt_data = trips_txt_data[(trips_txt_data['route_id']=='Bondi Junction to Waterfall or Cronull') |  (trips_txt_data['route_direction']=='Waterfall or Cronulla to Bondi Junction')]

route_ids=['L80','L71a','L71b','L72','L75','L81','L82a','L82b','L83a','L83b','L84a','L84b','L85','L86a','L86b','L87a','L87b','L88a','L88b']


sorted_trips_txt_data = trips_txt_data[trips_txt_data['route_id'].isin(route_ids)]

sorted_trips_txt_data

# %% Cell 20
routes_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/routes.txt'
routes_txt_data = pd.read_csv(routes_txt_path)
#trips_txt_data
#filtered_trips_txt_data = trips_txt_data[(trips_txt_data['route_id']=='Bondi Junction to Waterfall or Cronull') |  (trips_txt_data['route_direction']=='Waterfall or Cronulla to Bondi Junction')]

route_ids=['L80','L71a','L71b','L72','L75','L81','L82a','L82b','L83a','L83b','L84a','L84b','L85','L86a','L86b','L87a','L87b','L88a','L88b']


sorted_routes_txt_data = routes_txt_data[routes_txt_data['route_id'].isin(route_ids)]

#sorted_routes_txt_data



route_ids0 = sorted_routes_txt_data['route_id'].unique()
print(route_ids0)
print(len(route_ids0))

# %% Cell 21
sorted_routes_txt_data.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/routes2.txt", index=False)

# %% Cell 22
shape_ids0 = sorted_trips_txt_data['shape_id'].unique()
print(shape_ids0)
print(len(shape_ids0))

# %% Cell 23
shapes_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/shapes.txt'
shapes_txt_data = pd.read_csv(shapes_txt_path)
#stop_times_txt_data

sorted_shapes_txt_data = shapes_txt_data[shapes_txt_data['shape_id'].isin(shape_ids0)]
sorted_shapes_txt_data

# %% Cell 24
sorted_shapes_txt_data.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/shapes2.txt", index=False)

# %% Cell 25
trip_ids0 = sorted_trips_txt_data['trip_id'].unique()
print(trip_ids0)
print(len(trip_ids0))

# %% Cell 26
#trip_ids = filtered_trips_txt_data0['trip_id'].unique()
#print(trip_ids)
#print(len(trip_ids))

# %% Cell 27
sorted_trips_txt_data.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/trips2.txt", index=False)

# %% Cell 28
stop_times_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/stop_times.txt'
stop_times_txt_data = pd.read_csv(stop_times_txt_path)
#stop_times_txt_data

sorted_stop_times_txt_data = stop_times_txt_data[stop_times_txt_data['trip_id'].isin(trip_ids0)]
sorted_stop_times_txt_data

# %% Cell 29
sorted_stop_times_txt_data.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/S6/stop_times2.txt", index=False)

# %% Cell 30
sorted_stop_times_txt_data1 = sorted_stop_times_txt_data[sorted_stop_times_txt_data['arrival_time'].str.startswith('08')]
sorted_stop_times_txt_data1

# %% Cell 31
trip_ids0 = sorted_stop_times_txt_data1['trip_id'].unique()
print(trip_ids0)
print(len(trip_ids0))

# %% Cell 32
def test_function(x):
    return x

print(test_function(5))

# %% Cell 33
from datetime import datetime, timedelta


def process_trip(trip_id):

    global stop_times_txt_data

    truth_condition = (stop_times_txt_data['stop_sequence'] == 1) & (stop_times_txt_data['stop_id'] != 2031201) & (stop_times_txt_data['stop_id'] != 2031202) & (stop_times_txt_data['trip_id'] == trip_id)
    if truth_condition.any():
        print('Not working for this trip')
        return 
    # Filter DataFrame for the specific trip_id
    #trip_df = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id].copy()
    filtered_row = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == 1)].copy()
    filtered_row1 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == 1)].copy()
    filtered_row2 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == 1)].copy()
 

   
    
    filtered_row['stop_id'] = 2034103
    filtered_row1['stop_id'] = 2034102
    filtered_row2['stop_id'] = 20312030



    filtered_row1['stop_sequence'] = 2
    filtered_row2['stop_sequence'] = 3


    filtered_row1['drop_off_type'] = 0
    filtered_row2['drop_off_type'] = 0
 
    
    arrival_time_str = filtered_row['arrival_time'].values[0]
    arrival_time = datetime.strptime(arrival_time_str, '%H:%M:%S')
    new_arrival_time = arrival_time - timedelta(minutes=6)
    new_arrival_time_str = new_arrival_time.strftime('%H:%M:%S')
    filtered_row['arrival_time'] = new_arrival_time_str

    departure_time_str = filtered_row['departure_time'].values[0]
    departure_time = datetime.strptime(departure_time_str, '%H:%M:%S')
    new_departure_time = departure_time - timedelta(minutes=6)
    new_departure_time_str = new_departure_time.strftime('%H:%M:%S')
    filtered_row['departure_time'] = new_departure_time_str




    arrival_time_str4 = filtered_row1['arrival_time'].values[0]
    arrival_time4 = datetime.strptime(arrival_time_str4, '%H:%M:%S')
    new_arrival_time4 = arrival_time4 - timedelta(minutes=4, seconds=5)
    new_arrival_time_str4 = new_arrival_time4.strftime('%H:%M:%S')
    filtered_row1['arrival_time'] = new_arrival_time_str4

    departure_time_str4 = filtered_row1['departure_time'].values[0]
    departure_time4 = datetime.strptime(departure_time_str4, '%H:%M:%S')
    new_departure_time4 = departure_time4 - timedelta(minutes=4)
    new_departure_time_str4 = new_departure_time4.strftime('%H:%M:%S')
    filtered_row1['departure_time'] = new_departure_time_str4


    arrival_time_str5 = filtered_row2['arrival_time'].values[0]
    arrival_time5 = datetime.strptime(arrival_time_str5, '%H:%M:%S')
    new_arrival_time5 = arrival_time5 - timedelta(minutes=2, seconds=5)
    new_arrival_time_str5 = new_arrival_time5.strftime('%H:%M:%S')
    filtered_row2['arrival_time'] = new_arrival_time_str5

    departure_time_str5 = filtered_row2['departure_time'].values[0]
    departure_time5 = datetime.strptime(departure_time_str5, '%H:%M:%S')
    new_departure_time5 = departure_time5 - timedelta(minutes=2)
    new_departure_time_str5 = new_departure_time5.strftime('%H:%M:%S')
    filtered_row2['departure_time'] = new_departure_time_str5


   


    condition = (stop_times_txt_data['trip_id'] == trip_id) & ((stop_times_txt_data['stop_id'] == 2031201) | (stop_times_txt_data['stop_id'] == 2031202))
    # Extract the current arrival time
    current_arrival_time_str1 = stop_times_txt_data.loc[condition, 'arrival_time'].values[0]
    # Convert the arrival time to a datetime object
    current_arrival_time1 = datetime.strptime(current_arrival_time_str1, '%H:%M:%S')
    # Subtract one minute
    new_arrival_time1 = current_arrival_time1 - timedelta(seconds=5)
    # Convert back to string
    new_arrival_time_str1 = new_arrival_time1.strftime('%H:%M:%S')
    # Update the DataFrame
    stop_times_txt_data.loc[condition, 'arrival_time'] = new_arrival_time_str1

    stop_times_txt_data.loc[condition, 'drop_off_type'] = 0

    stop_times_txt_data.loc[stop_times_txt_data['trip_id']==trip_id, 'stop_sequence'] += 3


    index_to_insert_before = stop_times_txt_data[((stop_times_txt_data['stop_id'] == 2031201) | (stop_times_txt_data['stop_id'] == 2031202)) & (stop_times_txt_data['trip_id']== trip_id)].index[0]

    # Step 2: Create the DataFrames for concatenation
    df_top = stop_times_txt_data.iloc[:index_to_insert_before]  # DataFrame before the insertion point
    df_bottom = stop_times_txt_data.iloc[index_to_insert_before:]  # DataFrame after the insertion point



    rows_to_insert = [filtered_row,filtered_row1,filtered_row2]

    insert_df = pd.concat(rows_to_insert, ignore_index=True)

    # Step 3: Insert the new row and concatenate
    stop_times_txt_data = pd.concat([df_top, insert_df, df_bottom], ignore_index=True).reset_index(drop=True)
    stop_tines_txt_data = stop_times_txt_data.drop_duplicates()
    
    #index_to_insert_before = stop_times_txt_data[stop_times_txt_data['stop_sequence'] == 0].index[0]
    #stop_times_txt_data.loc[index_to_insert_before] = filtered_row.iloc[0]
    #stop_times_txt_data = pd.concat([stop_times_txt_data.iloc[:index_to_insert_before], filtered_row, stop_times_txt_data.iloc[index_to_insert_before:]]).reset_index(drop=True)


       
    
    return

# %% Cell 34
process_trip('38795-71090:1000')

# %% Cell 35
print(trip_ids0[0])

# %% Cell 36
ticker = 0

for trip in trip_ids0:
    process_trip(trip)
    ticker +=1
    print(ticker)

# %% Cell 37
test_output = stop_times_txt_data[stop_times_txt_data['trip_id']=='38795-71090:1000']
test_output

# %% Cell 38
print(test_output['arrival_time'].dtype)

# %% Cell 39
unique_types = stop_times_txt_data['departure_time'].map(type).unique()
print("Unique data types in the column:", unique_types)

# %% Cell 40
filtered_trips_txt_data1 = filtered_trips_txt_data[filtered_trips_txt_data['direction_id']==0]
filtered_trips_txt_data1

# %% Cell 41
trip_ids1 = filtered_trips_txt_data1['trip_id'].unique()
print(trip_ids1)
print(len(trip_ids1))

# %% Cell 42

sorted_stop_times_txt_data1 = stop_times_txt_data[stop_times_txt_data['trip_id'].isin(trip_ids1)]
sorted_stop_times_txt_data1

# %% Cell 43
sorted_stop_times_txt_data2 = sorted_stop_times_txt_data1[sorted_stop_times_txt_data1['arrival_time'].str.startswith('08')]
sorted_stop_times_txt_data2

# %% Cell 44
trip_ids2 = sorted_stop_times_txt_data2['trip_id'].unique()
print(trip_ids2)
print(len(trip_ids2))

# %% Cell 45
final_stop_sequence = stop_times_txt_data[stop_times_txt_data['trip_id'] == '38795-71092:1000']['stop_sequence'].max()
final_stop_sequence

# %% Cell 46
def process_trip1(trip_id):

    global stop_times_txt_data

    final_stop_sequence = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id]['stop_sequence'].max()

    truth_condition = (stop_times_txt_data['stop_sequence'] == final_stop_sequence) & (stop_times_txt_data['stop_id'] != 2031201) & (stop_times_txt_data['stop_id'] != 2031202) & (stop_times_txt_data['trip_id'] == trip_id)
    if truth_condition.any():
        'Does not work for this Trip'
        return
    # Filter DataFrame for the specific trip_id
    #trip_df = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id].copy()
    filtered_row = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == final_stop_sequence)].copy()
    filtered_row1 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == final_stop_sequence)].copy()
    filtered_row2 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == final_stop_sequence)].copy()


    
    filtered_row['stop_id'] = 20312030
    filtered_row1['stop_id'] = 2034102
    filtered_row2['stop_id'] = 2034103
 
    
    arrival_time_str = filtered_row['arrival_time'].values[0]
    arrival_time = datetime.strptime(arrival_time_str, '%H:%M:%S')
    new_arrival_time = arrival_time + timedelta(minutes=2)
    new_arrival_time_str = new_arrival_time.strftime('%H:%M:%S')
    filtered_row['arrival_time'] = new_arrival_time_str

    departure_time_str = filtered_row['departure_time'].values[0]
    departure_time = datetime.strptime(departure_time_str, '%H:%M:%S')
    new_departure_time = departure_time + timedelta(minutes=2, seconds=5)
    new_departure_time_str = new_departure_time.strftime('%H:%M:%S')
    filtered_row['departure_time'] = new_departure_time_str


    arrival_time_str3 = filtered_row1['arrival_time'].values[0]
    arrival_time3 = datetime.strptime(arrival_time_str3, '%H:%M:%S')
    new_arrival_time3 = arrival_time3 + timedelta(minutes=4)
    new_arrival_time_str3 = new_arrival_time3.strftime('%H:%M:%S')
    filtered_row1['arrival_time'] = new_arrival_time_str3

    departure_time_str3 = filtered_row1['departure_time'].values[0]
    departure_time3 = datetime.strptime(departure_time_str3, '%H:%M:%S')
    new_departure_time3 = departure_time3 + timedelta(minutes=4, seconds=5)
    new_departure_time_str3 = new_departure_time3.strftime('%H:%M:%S')
    filtered_row1['departure_time'] = new_departure_time_str3


    arrival_time_str4 = filtered_row2['arrival_time'].values[0]
    arrival_time4 = datetime.strptime(arrival_time_str4, '%H:%M:%S')
    new_arrival_time4 = arrival_time4 + timedelta(minutes=6)
    new_arrival_time_str4 = new_arrival_time4.strftime('%H:%M:%S')
    filtered_row2['arrival_time'] = new_arrival_time_str4

    departure_time_str4 = filtered_row2['departure_time'].values[0]
    departure_time4 = datetime.strptime(departure_time_str4, '%H:%M:%S')
    new_departure_time4 = departure_time4 + timedelta(minutes=6)
    new_departure_time_str4 = new_departure_time4.strftime('%H:%M:%S')
    filtered_row2['departure_time'] = new_departure_time_str4

    

    

    filtered_row['stop_sequence'] =filtered_row['stop_sequence'] + 1
    filtered_row1['stop_sequence'] =filtered_row1['stop_sequence'] + 2
    filtered_row2['stop_sequence'] =filtered_row2['stop_sequence'] + 3

  

    filtered_row['pickup_type'] = 0
    filtered_row1['pickup_type'] = 0




    condition = (stop_times_txt_data['trip_id'] == trip_id) & ((stop_times_txt_data['stop_id'] == 2031201) | (stop_times_txt_data['stop_id'] == 2031202)) 
    # Extract the current arrival time
    current_arrival_time_str1 = stop_times_txt_data.loc[condition, 'arrival_time'].values[0]
    # Convert the arrival time to a datetime object
    current_arrival_time1 = datetime.strptime(current_arrival_time_str1, '%H:%M:%S')
    # Subtract one minute
    new_arrival_time1 = current_arrival_time1 - timedelta(minutes=1)
    # Convert back to string
    new_arrival_time_str1 = new_arrival_time1.strftime('%H:%M:%S')
    # Update the DataFrame
    stop_times_txt_data.loc[condition, 'arrival_time'] = new_arrival_time_str1

    stop_times_txt_data.loc[condition, 'pickup_type'] = 0


    rows_to_insert = [filtered_row,filtered_row1,filtered_row2]

    insert_df = pd.concat(rows_to_insert, ignore_index=True)

 


    index_to_insert_after = stop_times_txt_data[((stop_times_txt_data['stop_id'] == 2031201) | (stop_times_txt_data['stop_id'] == 2031202)) & (stop_times_txt_data['trip_id']== trip_id)].index[0]

    # Step 2: Create the DataFrames for concatenation
    df_top = stop_times_txt_data.iloc[:index_to_insert_after + 1]  # DataFrame before the insertion point
    df_bottom = stop_times_txt_data.iloc[index_to_insert_after + 1:]  # DataFrame after the insertion point

    # Step 3: Insert the new row and concatenate
    stop_times_txt_data = pd.concat([df_top, insert_df, df_bottom], ignore_index=True).reset_index(drop=True)
    stop_tines_txt_data = stop_times_txt_data.drop_duplicates()
    
    #index_to_insert_before = stop_times_txt_data[stop_times_txt_data['stop_sequence'] == 0].index[0]
    #stop_times_txt_data.loc[index_to_insert_before] = filtered_row.iloc[0]
    #stop_times_txt_data = pd.concat([stop_times_txt_data.iloc[:index_to_insert_before], filtered_row, stop_times_txt_data.iloc[index_to_insert_before:]]).reset_index(drop=True)


       
    
    return

# %% Cell 47
ticker = 0

for trip1 in trip_ids2:
    process_trip1(trip1)
    ticker +=1
    print(ticker)

# %% Cell 48
process_trip1('38795-71092:1000')

# %% Cell 49
test_output = stop_times_txt_data[stop_times_txt_data['trip_id']=='43277-11118:1000']
test_output

# %% Cell 50
stop_times_txt_data.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/new_base_case_with_smw_v4_lightrail/stop_times.txt", index=False)

# %% Cell 51
shapefile_path_gtfs1 = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/extensive_lightrail_v2.zip'

# %% Cell 52
import r5py
import osmnx as ox

#G=ox.graph_from_file(shapefile_path_osm, simplify = False)

transport_network = r5py.TransportNetwork(
    shapefile_path_osm,
    [
        shapefile_path_gtfs1,
    ]
)

# %% Cell 53
import datetime


travel_time_matrix = r5py.TravelTimeMatrixComputer(
    transport_network,
    origins=origins,
    destinations=destinations,
    transport_modes=[r5py.TransportMode.TRANSIT, r5py.TransportMode.WALK],
    departure=datetime.datetime(2024, 8, 28, 8, 00, 00),
    departure_time_window=datetime.timedelta(hours=1),
    snap_to_network=True
).compute_travel_times()

# %% Cell 54
travel_time_matrix

# %% Cell 55
test_location = 146

travel_times_to_centre = travel_time_matrix[travel_time_matrix["to_id"] == test_location].copy()
travel_times_to_centre = travel_times_to_centre.set_index("from_id")[["travel_time"]]

grid_with_travel_time_to_centre = (
    filtered_gdf2.set_index("id").join(travel_times_to_centre)
)

grid_with_travel_time_to_centre

# %% Cell 56
grid_with_travel_time_to_centre.explore(
    column="travel_time",
    cmap="RdYlGn",
    tiles="CartoDB.Positron",
)

# %% Cell 57
median_travel_times = travel_time_matrix.groupby("from_id")["travel_time"].median()
median_travel_times

# %% Cell 58
grid_with_median_travel_times = (
    filtered_gdf2.set_index("id").join(median_travel_times)
)

grid_with_median_travel_times.explore(
    column="travel_time", 
    cmap="RdYlGn_r",
    tiles="CartoDB.Positron",
)

# %% Cell 59


merged_traveltime_matrix = pd.merge(travel_time_matrix, filtered_gdf2, left_on='to_id', right_on='TZ16_CODE', how='left')

merged_traveltime_matrix

# %% Cell 60
threshold =30
# Count the number of opportunities from each grid cell
opportunities = merged_traveltime_matrix.loc[merged_traveltime_matrix["travel_time"]<=threshold].groupby("from_id")["EMP_2016"].sum().reset_index()

# Rename the column for more intuitive one
opportunities = opportunities.rename(columns={"from_id": "num_opportunities"})

opportunities

# %% Cell 61
opportunities2 = filtered_gdf2.merge(opportunities, left_on="id", right_on="num_opportunities")
opportunities2

# %% Cell 62
opportunities.to_csv("C:/Users/m1llz/Downloads/opportunities_2001.csv", index=False)

# %% Cell 63
import matplotlib.pyplot as plt

ax = opportunities2.plot(column="EMP_2016_y", figsize=(10,5), legend=True)
ax.set_title(f"Number of opportunities within {threshold} minutes."); 

plt.set_cmap('RdYlGn')
plt.show()
#plt.savefig('C:/Users/m1llz/Downloads/plot.jpg', format='jpg')

# %% Cell 64
opportunities2['APW'] =(opportunities2['EMP_2016_x'] * opportunities2['EMP_2016_y'])/opportunities2['EMP_2016_x'].sum()

#opportunities2
total_APW = opportunities2['APW'].sum()
print(total_APW)

# %% Cell 65


# %% Cell 66


# %% Cell 67

