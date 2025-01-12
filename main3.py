import subprocess
import geopandas as gpd
from shapely.geometry import box, Point
import io
import numpy as np

# Constants for file paths and configurations
INPUT_FOLDER = "./input/"
OUTPUT_FOLDER = "./output"
TEIGHA_PATH = "C:/Program Files/ODA/ODAFileConverter 25.11.0/ODAFileConverter.exe"
OUTVER = "ACAD2018"
OUTFORMAT = "DXF"
RECURSIVE = "0"
AUDIT = "1"
INPUTFILTER = "*.DWG"

# Step 1: Convert DWG to DXF using ODA File Converter
cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]
subprocess.run(cmd, shell=True)

# Step 2: Load the converted DXF file using GeoPandas
data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")
data['geom_type'] = data.geometry.type
data.set_crs(epsg=4326, inplace=True)  # Assuming the original CRS is WGS 84

# Step 3: Calculate the bounding box and crop the data
bounding_box_polygon = box(637000, 3902000, 672000, 3919000)
cropped_data = data[data.geometry.intersects(bounding_box_polygon)]
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']

# Step 4: Assign a specific coordinate to a new point and create a GeoDataFrame
latitude = 48.549769
longitude = 18.220756
point = Point(longitude, latitude)
point_gdf = gpd.GeoDataFrame([point], columns=['geometry'], crs='EPSG:4326')

# Step 5: Reproject the existing data and the new point to Austria's CRS (EPSG:31287)
austria_crs = 'EPSG:31287'
data_lines = data_lines.to_crs(austria_crs)
data_points = data_points.to_crs(austria_crs)
point_gdf = point_gdf.to_crs(austria_crs)

# Step 6: Save the reprojected shapefiles and the new point shapefile
data_lines.to_file("./output/cropped_lines.shp")
data_points.to_file("./output/cropped_points.shp")
point_gdf.to_file("./output/assigned_location.shp")

print("Reprojection and coordinate assignment completed!")
