# Exported from THESISCODE 1974 Proposal.ipynb. Outputs removed; execution order preserved where present.


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
#print(sorted_gdf.dtypes)
#print(csv_job_data.dtypes)

if sorted_gdf.iloc[50,0] == csv_job_data.iloc[50,0]:
    print('yay')
    print(sorted_gdf.iloc[50,0])
    print(csv_job_data.iloc[50,0])

else:
    print('oh no')

# %% Cell 6
common_column = 'TZ16_CODE'
columns_to_include =['SA2_Name16', 'SA3_Name16', 'SA4_Name16', 'LGA_Name18', 'EMP_2016'] 

# Ensure both have the same column names for the common identifier

#sorted_gdf.rename(columns={'TZ16_CODE': common_column}, inplace=True)
#csv_job_data.rename(columns={'TZ16_CODE': common_column}, inplace=True)



# Perform merge based on the common identifier and selected columns
merged_data = sorted_gdf.join(csv_job_data[columns_to_include])
merged_data

# %% Cell 7



import matplotlib.pyplot as plt


filtered_gdf = merged_data[merged_data["SA4_Name16"].str.contains('Sydney')]

filtered_gdf


#filtered_gdf.plot()

#plt.show()

# %% Cell 8
shapefile_path_osm = 'C:/Users/m1llz/Downloads/UNI FILES/sydney-osm-withsydneymetrowest.osm.pbf'

#"C:\Users\m1llz\Downloads\UNI FILES\V2OSM-plswork.osm.pbf"
#"C:\Users\m1llz\Downloads\UNI FILES\UNISTUFF V2\full_greater_sydney_gtfs_static_0_editing.zip"
#"C:\Users\m1llz\Downloads\UNI FILES\UNISTUFF V2\full_greater_sydney_gtfs_static_0 (1).zip"

# %% Cell 9
filtered_gdf.explore()

# %% Cell 10
filtered_gdf.loc[:, 'id'] = filtered_gdf['TZ16_CODE'].copy()

# %% Cell 11
filtered_gdf

# %% Cell 12
filtered_gdf2 = filtered_gdf.to_crs('epsg:3308')
filtered_gdf2

# %% Cell 13
origins = filtered_gdf2.copy()
origins["geometry"] = origins.geometry.centroid
destinations = filtered_gdf2.copy()
destinations["geometry"] = destinations.geometry.centroid

# %% Cell 14
print(filtered_gdf2.loc[0])
print(filtered_gdf2.loc[2565])

# %% Cell 15
trips_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/new_base_case_with_smw_v4_1974edits/trips.txt'
trips_txt_data = pd.read_csv(trips_txt_path)
#trips_txt_data
#filtered_trips_txt_data = trips_txt_data[(trips_txt_data['route_id']=='Bondi Junction to Waterfall or Cronull') |  (trips_txt_data['route_direction']=='Waterfall or Cronulla to Bondi Junction')]

#"C:\Users\m1llz\Downloads\UNI FILES\UNISTUFF V2\"
filtered_trips_txt_data = trips_txt_data[trips_txt_data['route_id']=='2-T4-sj2-1']


filtered_trips_txt_data

# %% Cell 16
filtered_trips_txt_data0 = filtered_trips_txt_data[filtered_trips_txt_data['direction_id']==0]
filtered_trips_txt_data0

# %% Cell 17
trip_ids = filtered_trips_txt_data0['trip_id'].unique()
print(trip_ids)
print(len(trip_ids))

# %% Cell 18
stop_times_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/new_base_case_with_smw_v4_1974edits/stop_times.txt'
stop_times_txt_data = pd.read_csv(stop_times_txt_path)
sorted_stop_times_txt_data = stop_times_txt_data[stop_times_txt_data['trip_id'].isin(trip_ids)]
sorted_stop_times_txt_data

# %% Cell 19
print(stop_times_txt_data['stop_id'].dtype)

# %% Cell 20
sorted_stop_times_txt_data1 = sorted_stop_times_txt_data[sorted_stop_times_txt_data['arrival_time'].str.startswith('08')]
sorted_stop_times_txt_data1

# %% Cell 21
trip_ids0 = sorted_stop_times_txt_data1['trip_id'].unique()
print(trip_ids0)
print(len(trip_ids0))

# %% Cell 22
def test_function(x):
    return x

print(test_function(5))

# %% Cell 23
from datetime import datetime, timedelta


def process_trip(trip_id):

    global stop_times_txt_data

    truth_condition = (stop_times_txt_data['stop_sequence'] == 1) & (stop_times_txt_data['stop_id'] != 202291) & (stop_times_txt_data['stop_id'] != 202292) & (stop_times_txt_data['trip_id'] == trip_id)
    if truth_condition.any():
        print('Not working for this trip')
        return 
    # Filter DataFrame for the specific trip_id
    #trip_df = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id].copy()
    filtered_row = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == 1)].copy()
    filtered_row1 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == 1)].copy()
    filtered_row2 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == 1)].copy()
    
    filtered_row['stop_id'] = 2000911
    filtered_row1['stop_id'] = 2000921
    filtered_row2['stop_id'] = 2000931


    filtered_row1['stop_sequence'] = 2
    filtered_row2['stop_sequence'] = 3

    filtered_row1['drop_off_type'] = 0
    filtered_row2['drop_off_type'] = 0
    
    arrival_time_str = filtered_row['arrival_time'].values[0]
    arrival_time = datetime.strptime(arrival_time_str, '%H:%M:%S')
    new_arrival_time = arrival_time - timedelta(minutes=7)
    new_arrival_time_str = new_arrival_time.strftime('%H:%M:%S')
    filtered_row['arrival_time'] = new_arrival_time_str

    departure_time_str = filtered_row['departure_time'].values[0]
    departure_time = datetime.strptime(departure_time_str, '%H:%M:%S')
    new_departure_time = departure_time - timedelta(minutes=7)
    new_departure_time_str = new_departure_time.strftime('%H:%M:%S')
    filtered_row['departure_time'] = new_departure_time_str




    arrival_time_str4 = filtered_row1['arrival_time'].values[0]
    arrival_time4 = datetime.strptime(arrival_time_str4, '%H:%M:%S')
    new_arrival_time4 = arrival_time4 - timedelta(minutes=6)
    new_arrival_time_str4 = new_arrival_time4.strftime('%H:%M:%S')
    filtered_row1['arrival_time'] = new_arrival_time_str4

    departure_time_str4 = filtered_row1['departure_time'].values[0]
    departure_time4 = datetime.strptime(departure_time_str4, '%H:%M:%S')
    new_departure_time4 = departure_time4 - timedelta(minutes=5,seconds=30)
    new_departure_time_str4 = new_departure_time4.strftime('%H:%M:%S')
    filtered_row1['departure_time'] = new_departure_time_str4


    arrival_time_str5 = filtered_row2['arrival_time'].values[0]
    arrival_time5 = datetime.strptime(arrival_time_str5, '%H:%M:%S')
    new_arrival_time5 = arrival_time5 - timedelta(minutes=4)
    new_arrival_time_str5 = new_arrival_time5.strftime('%H:%M:%S')
    filtered_row2['arrival_time'] = new_arrival_time_str5

    departure_time_str5 = filtered_row2['departure_time'].values[0]
    departure_time5 = datetime.strptime(departure_time_str5, '%H:%M:%S')
    new_departure_time5 = departure_time5 - timedelta(minutes=3,seconds=30)
    new_departure_time_str5 = new_departure_time5.strftime('%H:%M:%S')
    filtered_row2['departure_time'] = new_departure_time_str5



    condition = (stop_times_txt_data['trip_id'] == trip_id) & ((stop_times_txt_data['stop_id'] == 202291) | (stop_times_txt_data['stop_id'] == 202292))
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

    stop_times_txt_data.loc[condition, 'drop_off_type'] = 0

    stop_times_txt_data.loc[stop_times_txt_data['trip_id']==trip_id, 'stop_sequence'] += 3


    index_to_insert_before = stop_times_txt_data[((stop_times_txt_data['stop_id'] == 202291) | (stop_times_txt_data['stop_id'] == 202292)) & (stop_times_txt_data['trip_id']== trip_id)].index[0]

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

# %% Cell 24
#process_trip('412B.1396.144.16.H.8.81851741')

# %% Cell 25
ticker = 0

for trip in trip_ids0:
    process_trip(trip)
    ticker +=1
    print(ticker)

# %% Cell 26
test_output = stop_times_txt_data[stop_times_txt_data['trip_id']=='412B.1396.144.16.H.8.81851741']
test_output

# %% Cell 27
print(test_output['arrival_time'].dtype)

# %% Cell 28
unique_types = stop_times_txt_data['departure_time'].map(type).unique()
print("Unique data types in the column:", unique_types)

# %% Cell 29
filtered_trips_txt_data1 = filtered_trips_txt_data[filtered_trips_txt_data['direction_id']==1]
filtered_trips_txt_data1

# %% Cell 30
trip_ids1 = filtered_trips_txt_data1['trip_id'].unique()
print(trip_ids1)
print(len(trip_ids1))

# %% Cell 31

sorted_stop_times_txt_data1 = stop_times_txt_data[stop_times_txt_data['trip_id'].isin(trip_ids1)]
sorted_stop_times_txt_data1

# %% Cell 32
sorted_stop_times_txt_data2 = sorted_stop_times_txt_data1[sorted_stop_times_txt_data1['arrival_time'].str.startswith('08')]
sorted_stop_times_txt_data2

# %% Cell 33
#sorted_stop_times_txt_data2.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/test_stop_times.csv", index=False)

# %% Cell 34
trip_ids2 = sorted_stop_times_txt_data2['trip_id'].unique()
print(trip_ids2)
print(len(trip_ids2))

# %% Cell 35
final_stop_sequence = stop_times_txt_data[stop_times_txt_data['trip_id'] == '602C.1904.101.2.T.8.81040236']['stop_sequence'].max()
final_stop_sequence

# %% Cell 36
def process_trip1(trip_id):

    global stop_times_txt_data

    final_stop_sequence = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id]['stop_sequence'].max()

    truth_condition = (stop_times_txt_data['stop_sequence'] == final_stop_sequence) & (stop_times_txt_data['stop_id'] != 202291) & (stop_times_txt_data['stop_id'] != 202292 ) & (stop_times_txt_data['trip_id'] == trip_id)
    if truth_condition.any():
        'Does not work for this Trip'
        return
    # Filter DataFrame for the specific trip_id
    #trip_df = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id].copy()
    filtered_row = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == final_stop_sequence)].copy()
    filtered_row1 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == final_stop_sequence)].copy()
    filtered_row2 = stop_times_txt_data[(stop_times_txt_data['trip_id'] == trip_id) & (stop_times_txt_data['stop_sequence'] == final_stop_sequence)].copy()
    
    filtered_row['stop_id'] = 2000911
    filtered_row1['stop_id'] = 2000921
    filtered_row2['stop_id'] = 2000931
    
    arrival_time_str = filtered_row['arrival_time'].values[0]
    arrival_time = datetime.strptime(arrival_time_str, '%H:%M:%S')
    new_arrival_time = arrival_time + timedelta(minutes=2)
    new_arrival_time_str = new_arrival_time.strftime('%H:%M:%S')
    filtered_row['arrival_time'] = new_arrival_time_str

    departure_time_str = filtered_row['departure_time'].values[0]
    departure_time = datetime.strptime(departure_time_str, '%H:%M:%S')
    new_departure_time = departure_time + timedelta(minutes=2,seconds=30)
    new_departure_time_str = new_departure_time.strftime('%H:%M:%S')
    filtered_row['departure_time'] = new_departure_time_str


    arrival_time_str3 = filtered_row1['arrival_time'].values[0]
    arrival_time3 = datetime.strptime(arrival_time_str3, '%H:%M:%S')
    new_arrival_time3 = arrival_time3 + timedelta(minutes=4)
    new_arrival_time_str3 = new_arrival_time3.strftime('%H:%M:%S')
    filtered_row1['arrival_time'] = new_arrival_time_str3

    departure_time_str3 = filtered_row1['departure_time'].values[0]
    departure_time3 = datetime.strptime(departure_time_str3, '%H:%M:%S')
    new_departure_time3 = departure_time3 + timedelta(minutes=4,seconds=30)
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



    condition = (stop_times_txt_data['trip_id'] == trip_id) & ((stop_times_txt_data['stop_id'] == 202291) | (stop_times_txt_data['stop_id'] == 202292))
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

 


    index_to_insert_after = stop_times_txt_data[((stop_times_txt_data['stop_id'] == 202291) | (stop_times_txt_data['stop_id'] == 202292)) & (stop_times_txt_data['trip_id']== trip_id)].index[0]

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

# %% Cell 37
ticker = 0

for trip1 in trip_ids2:
    process_trip1(trip1)
    ticker +=1
    print(ticker)

# %% Cell 38
#process_trip1('606C.807.155.124.T.8.81897563')

# %% Cell 39
test_output = stop_times_txt_data[stop_times_txt_data['trip_id']=='606C.807.155.124.T.8.81897563']
test_output

# %% Cell 40
stop_times_txt_data.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/new_base_case_with_smw_v4_1974edits/stop_times.txt", index=False)

# %% Cell 41
stop_times_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/improved-gtfs-greater-sydney-editing/stop_times.txt'
stop_times_txt_data = pd.read_csv(stop_times_txt_path)
#trips_txt_data
#filtered_trips_txt_data = trips_txt_data[(trips_txt_data['route_id']=='Bondi Junction to Waterfall or Cronull') |  (trips_txt_data['route_direction']=='Waterfall or Cronulla to Bondi Junction')]

filtered_stop_times_txt_data = stop_times_txt_data[stop_times_txt_data['trip_id']=='2330-758328c5e35a7d522e99']


filtered_stop_times_txt_data

# %% Cell 42
filtered_stop_times_txt_data['stop_sequence'] =filtered_stop_times_txt_data['stop_sequence'].astype(int)+ 1
filtered_stop_times_txt_data['stop_sequence'] =filtered_stop_times_txt_data['stop_sequence'].astype(str)
filtered_stop_times_txt_data




#filtered_stop_times_txt_data['stop_sequence']


#filtered_stop_times_txt_data_edited = pd.to_numeric(filtered_stop_times_txt_data['stop_sequence'])
#filtered_stop_times_txt_data_edited['stop_sequence']

#filtered_stop_times_txt_data_edited =filtered_stop_times_txt_data['stop_sequence'].astype(int)+ 1
#filtered_stop_times_txt_data_edited['stop_sequence'].dtype


#filtered_stop_times_txt_data_edited= filtered_stop_times_txt_data_edited['stop_sequence'].astype(str)
#filtered_stop_times_txt_data_edited

# %% Cell 43
import pandas as pd
shape_txt_path = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/improved-gtfs-greater-sydney-editingV2/shapes.txt'
shape_txt_data = pd.read_csv(shape_txt_path)

#shape_txt_data
sorted_shape_txt_data = shape_txt_data[shape_txt_data['shape_id'].str.contains('T4', na=False)]
sorted_shape_txt_data

# %% Cell 44
print(shape_txt_data['shape_pt_lat'].dtype)

# %% Cell 45
list_of_shapes = sorted_shape_txt_data['shape_id'].unique()
print(list_of_shapes)
print(len(sorted_shape_txt_data['shape_id'].unique()))

# %% Cell 46
shape_txt_data[shape_txt_data['shape_id']=='2330-2-T4-sj2-1.87.R']

# %% Cell 47
def process_shape(shape_id):

    global shape_txt_data

    final_shape_pt_sequence = shape_txt_data[shape_txt_data['shape_id'] == shape_id]['shape_pt_sequence'].max()
    #print(final_shape_pt_sequence)

    truth_condition = (shape_txt_data['shape_pt_sequence'] == final_shape_pt_sequence) & (shape_txt_data['shape_pt_lat'] != -33.891298) & (shape_txt_data['shape_pt_lat'] != -33.891063 ) & (shape_txt_data['shape_id'] == shape_id)
    if truth_condition.any():
        return #'Not Recognised'
    # Filter DataFrame for the specific trip_id
    #trip_df = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id].copy()
    filtered_row = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == final_shape_pt_sequence)].copy()

    filtered_row['shape_pt_lat'] = -33.888896
    filtered_row['shape_pt_lon'] = 151.257401
    filtered_row['shape_pt_sequence']= filtered_row['shape_pt_sequence'] + 1
    filtered_row['shape_dist_traveled'] = filtered_row['shape_dist_traveled'] + 867.2
    
    filtered_row1 = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == final_shape_pt_sequence)].copy()

    filtered_row1['shape_pt_lat'] = -33.887661
    filtered_row1['shape_pt_lon'] = 151.264881
    filtered_row1['shape_pt_sequence']= filtered_row1['shape_pt_sequence'] + 2
    filtered_row1['shape_dist_traveled'] = filtered_row1['shape_dist_traveled'] + 1571.2

    
    filtered_row2 = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == final_shape_pt_sequence)].copy()

    filtered_row2['shape_pt_lat'] = -33.885028
    filtered_row2['shape_pt_lon'] = 151.268158
    filtered_row2['shape_pt_sequence']= filtered_row2['shape_pt_sequence'] + 3
    filtered_row2['shape_dist_traveled'] = filtered_row2['shape_dist_traveled'] + 1991.2


    
    filtered_row3 = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == final_shape_pt_sequence)].copy()

    filtered_row3['shape_pt_lat'] = -33.885430
    filtered_row3['shape_pt_lon'] = 151.275678
    filtered_row3['shape_pt_sequence']= filtered_row3['shape_pt_sequence'] + 4
    filtered_row3['shape_dist_traveled'] = filtered_row3['shape_dist_traveled'] + 2686


    


 

    
    index_to_insert_after = shape_txt_data[((shape_txt_data['shape_pt_lat'] == -33.891298) | (shape_txt_data['shape_pt_lat'] == -33.891063)) & (shape_txt_data['shape_id']== shape_id)].index[0]

    # Step 2: Create the DataFrames for concatenation
    df_top = shape_txt_data.iloc[:index_to_insert_after + 1]  # DataFrame before the insertion point
    df_bottom = shape_txt_data.iloc[index_to_insert_after + 1:]  # DataFrame after the insertion point

    rows_to_insert = [filtered_row,filtered_row1,filtered_row2,filtered_row3]

    insert_df = pd.concat(rows_to_insert, ignore_index=True)
    
    # Step 3: Insert the new row and concatenate
    shape_txt_data = pd.concat([df_top, insert_df, df_bottom], ignore_index=True).reset_index(drop=True)
    #shape_txt_data = pd.concat([filtered_row, filtered_row1, df_bottom], ignore_index=True).reset_index(drop=True)
    #shape_txt_data = pd.concat([filtered_row1, filtered_row2, df_bottom], ignore_index=True).reset_index(drop=True)
    #shape_txt_data = pd.concat([filtered_row2, filtered_row3, df_bottom], ignore_index=True).reset_index(drop=True)
    
    
    shape_txt_data = shape_txt_data.drop_duplicates()
    
    #index_to_insert_before = stop_times_txt_data[stop_times_txt_data['stop_sequence'] == 0].index[0]
    #stop_times_txt_data.loc[index_to_insert_before] = filtered_row.iloc[0]
    #stop_times_txt_data = pd.concat([stop_times_txt_data.iloc[:index_to_insert_before], filtered_row, stop_times_txt_data.iloc[index_to_insert_before:]]).reset_index(drop=True)
    


       
    
    return #shape_txt_data[shape_txt_data['shape_id']==shape_id]

# %% Cell 48
#process_shape('2330-2-T4-sj2-1.87.R')

# %% Cell 49
def process_shape1(shape_id):

    global shape_txt_data

    

    truth_condition = (shape_txt_data['shape_pt_sequence'] == 0) & (shape_txt_data['shape_pt_lat'] != -33.891298) & (shape_txt_data['shape_pt_lat'] != -33.891063 ) & (shape_txt_data['shape_id'] == shape_id)
    if truth_condition.any():
        return #'Not Recognised'
    # Filter DataFrame for the specific trip_id
    #trip_df = stop_times_txt_data[stop_times_txt_data['trip_id'] == trip_id].copy()
    filtered_row = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == 0)].copy()

    filtered_row['shape_pt_lat'] = -33.885430
    filtered_row['shape_pt_lon'] = 151.275678
    #filtered_row['shape_pt_sequence']= filtered_row['shape_pt_sequence'] - 4
    #filtered_row['shape_dist_traveled'] = filtered_row['shape_dist_traveled'] + 867.2
    
    filtered_row1 = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == 0)].copy()

    filtered_row1['shape_pt_lat'] = -33.885028
    filtered_row1['shape_pt_lon'] = 151.268158
    filtered_row1['shape_pt_sequence']= filtered_row1['shape_pt_sequence'] + 1
    filtered_row1['shape_dist_traveled'] = filtered_row1['shape_dist_traveled'] + 694.8 

    
    filtered_row2 = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == 0)].copy()

    filtered_row2['shape_pt_lat'] = -33.887661
    filtered_row2['shape_pt_lon'] = 151.264881
    filtered_row2['shape_pt_sequence']= filtered_row2['shape_pt_sequence'] + 2
    filtered_row2['shape_dist_traveled'] = filtered_row2['shape_dist_traveled'] + 420 + 694.8 


    
    filtered_row3 = shape_txt_data[(shape_txt_data['shape_id'] == shape_id) & (shape_txt_data['shape_pt_sequence'] == 0)].copy()

    filtered_row3['shape_pt_lat'] = -33.888896
    filtered_row3['shape_pt_lon'] = 151.257401
    filtered_row3['shape_pt_sequence']= filtered_row3['shape_pt_sequence'] + 3
    filtered_row3['shape_dist_traveled'] = filtered_row3['shape_dist_traveled'] + 704 + 420 + 694.8 


    shape_txt_data.loc[shape_txt_data['shape_id']==shape_id, 'shape_pt_sequence'] += 4
    shape_txt_data.loc[shape_txt_data['shape_id']==shape_id, 'shape_dist_traveled'] += 2686


    


 

    
    index_to_insert_before = shape_txt_data[((shape_txt_data['shape_pt_lat'] == -33.891298) | (shape_txt_data['shape_pt_lat'] == -33.891063)) & (shape_txt_data['shape_id']== shape_id)].index[0]

    # Step 2: Create the DataFrames for concatenation
    df_top = shape_txt_data.iloc[:index_to_insert_before]  # DataFrame before the insertion point
    df_bottom = shape_txt_data.iloc[index_to_insert_before:]  # DataFrame after the insertion point

    rows_to_insert = [filtered_row,filtered_row1,filtered_row2,filtered_row3]

    insert_df = pd.concat(rows_to_insert, ignore_index=True)
    
    # Step 3: Insert the new row and concatenate
    shape_txt_data = pd.concat([df_top, insert_df, df_bottom], ignore_index=True).reset_index(drop=True)
    #shape_txt_data = pd.concat([filtered_row, filtered_row1, df_bottom], ignore_index=True).reset_index(drop=True)
    #shape_txt_data = pd.concat([filtered_row1, filtered_row2, df_bottom], ignore_index=True).reset_index(drop=True)
    #shape_txt_data = pd.concat([filtered_row2, filtered_row3, df_bottom], ignore_index=True).reset_index(drop=True)
    
    
    shape_txt_data = shape_txt_data.drop_duplicates()
    
    #index_to_insert_before = stop_times_txt_data[stop_times_txt_data['stop_sequence'] == 0].index[0]
    #stop_times_txt_data.loc[index_to_insert_before] = filtered_row.iloc[0]
    #stop_times_txt_data = pd.concat([stop_times_txt_data.iloc[:index_to_insert_before], filtered_row, stop_times_txt_data.iloc[index_to_insert_before:]]).reset_index(drop=True)
    


       
    
    return #shape_txt_data[shape_txt_data['shape_id']==shape_id]

# %% Cell 50
#process_shape1('2330-2-T4-sj2-1.161.H')

# %% Cell 51
ticker = 0

for shape in list_of_shapes:
    process_shape(shape)
    ticker +=1
    print(ticker)

# %% Cell 52
ticker = 0

for shape in list_of_shapes:
    process_shape1(shape)
    ticker +=1
    print(ticker)

# %% Cell 53
test_output = shape_txt_data[shape_txt_data['shape_id']=='2330-2-T4-sj2-1.238.H']
test_output

# %% Cell 54
shape_txt_data.to_csv("C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/improved-gtfs-greater-sydney-editingV2/shapes.txt", index=False)

# %% Cell 55
shapefile_path_gtfs1 = 'C:/Users/m1llz/Downloads/UNI FILES/UNISTUFF V2/1974_v2.zip'

# %% Cell 56
import r5py
import osmnx as ox

#G=ox.graph_from_file(shapefile_path_osm, simplify = False)

transport_network = r5py.TransportNetwork(
    shapefile_path_osm,
    [
        shapefile_path_gtfs1,
    ]
)

# %% Cell 57
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

# %% Cell 58
travel_time_matrix

# %% Cell 59
test_location = 146

travel_times_to_centre = travel_time_matrix[travel_time_matrix["to_id"] == test_location].copy()
travel_times_to_centre = travel_times_to_centre.set_index("from_id")[["travel_time"]]

grid_with_travel_time_to_centre = (
    filtered_gdf2.set_index("id").join(travel_times_to_centre)
)

grid_with_travel_time_to_centre

# %% Cell 60
grid_with_travel_time_to_centre.explore(
    column="travel_time",
    cmap="RdYlGn",
    tiles="CartoDB.Positron",
)

# %% Cell 61
median_travel_times = travel_time_matrix.groupby("from_id")["travel_time"].median()
median_travel_times

# %% Cell 62
grid_with_median_travel_times = (
    filtered_gdf2.set_index("id").join(median_travel_times)
)

grid_with_median_travel_times.explore(
    column="travel_time", 
    cmap="RdYlGn_r",
    tiles="CartoDB.Positron",
)

# %% Cell 63


merged_traveltime_matrix = pd.merge(travel_time_matrix, filtered_gdf2, left_on='to_id', right_on='TZ16_CODE', how='left')

merged_traveltime_matrix

# %% Cell 64
threshold =60
# Count the number of opportunities from each grid cell
opportunities = merged_traveltime_matrix.loc[merged_traveltime_matrix["travel_time"]<=threshold].groupby("from_id")["EMP_2016"].sum().reset_index()

# Rename the column for more intuitive one
opportunities = opportunities.rename(columns={"from_id": "num_opportunities"})

opportunities

# %% Cell 65
opportunities2 = filtered_gdf2.merge(opportunities, left_on="id", right_on="num_opportunities")
opportunities2

# %% Cell 66
opportunities.to_csv("C:/Users/m1llz/Downloads/opportunities_2001.csv", index=False)

# %% Cell 67
import matplotlib.pyplot as plt

ax = opportunities2.plot(column="EMP_2016_y", figsize=(10,5), legend=True)
ax.set_title(f"Number of opportunities within {threshold} minutes."); 
ax.invert_yaxis()
ax.invert_xaxis()
plt.set_cmap('RdYlGn')
plt.show()
#plt.savefig('C:/Users/m1llz/Downloads/plot.jpg', format='jpg')

# %% Cell 68
opportunities2['APW'] =(opportunities2['EMP_2016_x'] * opportunities2['EMP_2016_y'])/opportunities2['EMP_2016_x'].sum()

#opportunities2
total_APW = opportunities2['APW'].sum()
print(total_APW)

# %% Cell 69


# %% Cell 70


# %% Cell 71

