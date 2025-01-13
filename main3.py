# import subprocess
# import geopandas as gpd
# import geopandas as gpd
# from shapely.geometry import box

# INPUT_FOLDER = "./input/"
# OUTPUT_FOLDER = "./output"
# TEIGHA_PATH = "C:/Program Files/ODA/ODAFileConverter 25.11.0/ODAFileConverter.exe"
# OUTVER = "ACAD2018"
# OUTFORMAT = "DXF"
# RECURSIVE = "0"
# AUDIT = "1"
# INPUTFILTER = "*.DWG"
# cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]
# subprocess.run(cmd, shell=True)
# data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")
# data['geom_type'] = data.geometry.type
# data.set_crs(epsg=4326, inplace=True)
# bounding_box = data.total_bounds
# min_x, min_y, max_x, max_y = bounding_box
# print(f"Bounding Box: {bounding_box}")
# bounding_box_polygon = box(637000, 3902000, 672000, 3919000)
# cropped_data = data[data.geometry.intersects(bounding_box_polygon)]
# data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
# data_points = cropped_data[cropped_data['geom_type'] == 'Point']
# data_lines.to_file("./output/cropped_lines.shp")
# data_points.to_file("./output/cropped_points.shp")
# print("Cropped data conversion completed!")

########################################################
import subprocess
import geopandas as gpd
from shapely.geometry import box

# Constants for file paths and configurations
INPUT_FOLDER = "./input/"
OUTPUT_FOLDER = "./output"
TEIGHA_PATH = "C:/Program Files/ODA/ODAFileConverter 25.11.0/ODAFileConverter.exe"
OUTVER = "ACAD2018"
OUTFORMAT = "DXF"
RECURSIVE = "0"
AUDIT = "1"
INPUTFILTER = "*.DWG"

# Specific coordinates to add
latitude = 5715364.95858
longitude = 4261022.33099

# Step 1: Convert DWG to DXF using ODA File Converter
cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]
subprocess.run(cmd, shell=True)

# Step 2: Load the converted DXF file using GeoPandas
data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")
data['geom_type'] = data.geometry.type
# data.set_crs(epsg=4326, inplace=True)  # Assuming the original CRS is WGS 84
data.set_crs(epsg=3857, inplace=True)  # Assuming the original CRS is WGS 84

# Step 3: Calculate the bounding box and crop the data
bounding_box = data.total_bounds  # Returns (minx, miny, maxx, maxy)
print(f"Bounding Box: {bounding_box}")
bounding_box_polygon = box(637000, 3902000, 672000, 3919000)
cropped_data = data[data.geometry.intersects(bounding_box_polygon)]
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']

# Step 4: Add the specific latitude and longitude to each feature
data_lines['latitude'] = latitude
data_lines['longitude'] = longitude

data_points['latitude'] = latitude
data_points['longitude'] = longitude

# Step 5: Save the shapefiles with added latitude and longitude
data_lines.to_file("./output/cropped_lines_with_lat_long.shp")
data_points.to_file("./output/cropped_points_with_lat_long.shp")

print("Cropped data conversion with specific latitude and longitude completed!")





