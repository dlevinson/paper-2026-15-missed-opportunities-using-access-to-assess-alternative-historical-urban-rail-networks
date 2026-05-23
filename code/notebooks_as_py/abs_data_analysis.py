# Exported from ABS_DATA_ANALYSIS.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import geopandas as gpd



shapefile_path = 'C:/Users/m1llz/Downloads/2016_SA1_shape/SA1_2016_AUST.dbf'



    
gdf = gpd.read_file(shapefile_path)

# %% Cell 2
gdf

# %% Cell 3
gdf = gdf[gdf['STATE_NAME'] == 'New South Wales']
gdf

# %% Cell 4
gdf = gdf.dropna(subset=['geometry'])
gdf

# %% Cell 5
import pandas as pd

csv_path1 = 'C:/Users/m1llz/Downloads/2016_GCP_SA1_for_NSW_short-header/2016 Census GCP Statistical Area 1 for NSW/2016Census_G02_NSW_SA1.csv'


csv_abs_data = pd.read_csv(csv_path1)

csv_abs_data

# %% Cell 6

