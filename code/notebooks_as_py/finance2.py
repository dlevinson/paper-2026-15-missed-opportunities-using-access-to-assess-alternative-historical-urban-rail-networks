# Exported from Finance2.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import pandas as pd

csv_path = 'C:/Users/m1llz/Downloads/test_data.csv'
csv_house_data = pd.read_csv(csv_path)
csv_house_data

# %% Cell 2
import geopandas as gpd
import pandas as pd

# Load the shapefile
shapefile_path = 'path/to/your/shapefile.shp'
gdf_shapes = gpd.read_file(shapefile_path)

# %% Cell 3
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


# Create a geometry column from latitude and longitude
geometry = [Point(lon, lat) for lon, lat in zip(csv_house_data['Longitude'], csv_house_data['Latitude'])]
real_estate_gdf = gpd.GeoDataFrame(csv_house_data, geometry=geometry)

# Set the same coordinate reference system (CRS) for both GeoDataFrames
real_estate_gdf.set_crs(epsg=4326, inplace=True)  # Assuming WGS84 for lat/lon
#accessibility_gdf.set_crs(epsg=4326, inplace=True)  # Ensure the CRS matches

# %% Cell 4
#real_estate_gdf.set_crs(epsg=4326, inplace=True)  # Set the original CRS to WGS84

# Step 3: Reproject to EPSG:3308
gdf_projected = real_estate_gdf.to_crs(epsg=3308)
gdf_projected

# %% Cell 5
csv_path1 = 'C:/Users/m1llz/Downloads/spatial_30mins.csv'
csv_job_data = pd.read_csv(csv_path1)

csv_job_data

#csv_job_data_dropped_nan = csv_job_data.dropna(axis=1, how='any')
#csv_job_data_dropped_nan

# %% Cell 6
#geometry = [Point(lon, lat) for lon, lat in zip(csv_house_data['Longitude'], csv_house_data['Latitude'])]
#real_estate_gdf = gpd.GeoDataFrame(csv_house_data, geometry=geometry)

# Set the same coordinate reference system (CRS) for both GeoDataFrames
#real_estate_gdf.set_crs(epsg=3308, inplace=True)  # Assuming WGS84 for lat/lon
#accessibility_gdf.set_crs(epsg=4326, inplace=True)  # Ensure the CRS matches




from shapely.wkt import loads  # Import for WKT conversion

# Step 1: Load the CSV file


# Step 2: Convert the geometry column to Shapely geometries
# Assuming the geometry column is named 'geometry' and in WKT format
csv_job_data['geometry'] = csv_job_data['geometry'].apply(loads)

# Step 3: Create a GeoDataFrame
gdf = gpd.GeoDataFrame(csv_job_data, geometry='geometry')

# Step 4: Set the CRS to EPSG:3308
gdf.set_crs(epsg=3308, inplace=True)

# Optionally, you can check the GeoDataFrame
gdf

# %% Cell 7
joined = gpd.sjoin(gdf_projected, gdf, how='left', predicate='within')

joined

# %% Cell 8
joined1 = joined.dropna(subset=['30 Mins'])
joined1

# %% Cell 9
start_date = '2009-01-01'
end_date = '2019-12-31'

# Filter the DataFrame based on the date range
joined_recent = joined1[(joined1['Date Sold'] >= start_date) & (joined1['Date Sold'] <= end_date)]

joined_recent

# %% Cell 10
def check_match(row):
    return any(part in row['Region'] for part in row['TZ16_NAME'].split())

# Apply the function to create a mask and filter the DataFrame
joined_recent['Match'] = joined_recent.apply(check_match, axis=1)
filtered_df = joined_recent[joined_recent['Match']]

# Drop the Match column if you don't need it
filtered_df = filtered_df.drop(columns=['Match'])
filtered_df

# %% Cell 11
filtered_df['Bathrooms'] = pd.to_numeric(filtered_df['Bathrooms'], errors='coerce')
filtered_df['Bedrooms'] = pd.to_numeric(filtered_df['Bedrooms'], errors='coerce')
filtered_df['CarSpaces'] = pd.to_numeric(filtered_df['CarSpaces'], errors='coerce')
filtered_df['Land Size'] = pd.to_numeric(filtered_df['Land Size'], errors='coerce')
#result_inner3['Median Weekly Income'] = pd.to_numeric(result_inner3['Median Weekly Income'], errors='coerce')

# %% Cell 12
filtered_df

# %% Cell 13
filtered_df2 = filtered_df.dropna(subset=['Bathrooms', 'Bedrooms', 'CarSpaces'], how='all')
filtered_df2

# %% Cell 14
filtered_df2['Bathrooms'] = filtered_df2['Bathrooms'].fillna(0)
filtered_df2['Bedrooms'] = filtered_df2['Bedrooms'].fillna(0)
filtered_df2['CarSpaces'] = filtered_df2['CarSpaces'].fillna(0)
#filtered_df2['Floor Size'] = filtered_df2['Floor Size'].fillna(0)
#rfiltered_df2['Land Size'] = filtered_df2['Land Size'].fillna(0)
filtered_df2

# %% Cell 15
house_result = filtered_df2[filtered_df2['Building Type'] == 'House']
house_result

# %% Cell 16
#house_result = house_result.dropna(subset=['Floor Size', 'Land Size'])
#csv1_house_data3

house_result['Floor Size'] = house_result['Floor Size'].astype(str).str.replace('m2', '', regex=False)

# Convert to integers (handling non-numeric values)
house_result['Floor Size'] = pd.to_numeric(house_result['Floor Size'], errors='coerce').fillna(0).astype(int)


#house_result['Land Size'] = house_result['Land Size'].astype(str).str.replace('m2', '', regex=False)

# Convert to integers (handling non-numeric values)
#house_result['Land Size'] = pd.to_numeric(house_result['Land Size'], errors='coerce').fillna(0).astype(int)


#house_result['Land Size'] = house_result['Floor Size'].str.replace('m2', '', regex=False).astype(int)
house_result= house_result[(house_result['Floor Size'] > 0)]
#house_result= house_result[(house_result['Land Size'] > 0)]
house_result

# %% Cell 17
filtered_df2 = pd.get_dummies(filtered_df2, columns=['Building Type'], drop_first=True)


'''
from sklearn.preprocessing import LabelEncoder


#label_encoder = LabelEncoder()
#filtered_df2['Building Type'] = label_encoder.fit_transform(filtered_df2['Building Type'])

# Output

'''
filtered_df2

# %% Cell 18
filtered_df2['Floor Size'] = filtered_df2['Floor Size'].astype(str).str.replace('m2', '', regex=False)

# Convert to integers (handling non-numeric values)
filtered_df2['Floor Size'] = pd.to_numeric(filtered_df2['Floor Size'], errors='coerce').fillna(0).astype(int)


#house_result['Land Size'] = house_result['Land Size'].astype(str).str.replace('m2', '', regex=False)

# Convert to integers (handling non-numeric values)
#house_result['Land Size'] = pd.to_numeric(house_result['Land Size'], errors='coerce').fillna(0).astype(int)


#house_result['Land Size'] = house_result['Floor Size'].str.replace('m2', '', regex=False).astype(int)
filtered_df2= filtered_df2[(filtered_df2['Floor Size'] > 0)]
#house_result= house_result[(house_result['Land Size'] > 0)]
filtered_df2

# %% Cell 19
filtered_df2 = filtered_df2.applymap(lambda x: 1 if x is True else 0 if x is False else x)

filtered_df2

# %% Cell 20
filtered_df2['Building Age'] =  2019 - filtered_df2['Year Built']
filtered_df2

# %% Cell 21
from datetime import datetime
base_date = datetime(2019, 12, 31)

filtered_df2['Date Sold'] = pd.to_datetime(filtered_df2['Date Sold'])

# Calculate the difference in years
filtered_df2['YearsSinceSell'] = (filtered_df2['Date Sold'] - base_date).dt.days / 365.25
filtered_df2

# %% Cell 22
filtered_df2= filtered_df2[(filtered_df2['Building Age'] > 0)]
filtered_df2= filtered_df2[(filtered_df2['YearsSinceSell'] < 0)]
filtered_df2

# %% Cell 23
import statsmodels.api as sm



Y = filtered_df2['Amount Sold']

# Independent variables (X1, X2, X3)
X = filtered_df2[['Building Type', 'Bedrooms', 'Bathrooms', 'CarSpaces', 'Floor Size', '30 Mins']]

X = sm.add_constant(X)

model = sm.OLS(Y, X)
results = model.fit()

# Show the summary
print(results.summary())

# %% Cell 24


Y = filtered_df2['Amount Sold']

# Independent variables (X1, X2, X3)
X = filtered_df2[['Bedrooms', 'Bathrooms', 'CarSpaces', 'Floor Size', '30 Mins', 'Building Type_Commercial',	'Building Type_House',	'Building Type_Land',	'Building Type_Rural',	'Building Type_Townhouse',	'Building Type_Unit',	'Building Type_Unknown', 'Building Age', 'YearsSinceSell']]

X = sm.add_constant(X)

model = sm.OLS(Y, X)
results = model.fit()

# Show the summary
print(results.summary())

# %% Cell 25
print(filtered_df2.dtypes)

# %% Cell 26

