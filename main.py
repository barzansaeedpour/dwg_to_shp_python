import subprocess
import geopandas as gpd


##################################### dwg to dxf
INPUT_FOLDER = "./input/"
OUTPUT_FOLDER = "./output"


TEIGHA_PATH = "C:/Program Files/ODA/ODAFileConverter 25.11.0/ODAFileConverter.exe"
OUTVER = "ACAD2018"
OUTFORMAT = "DXF"
RECURSIVE = "0"
AUDIT = "1"
INPUTFILTER = "*.DWG"

# Command to run
cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]

# Run
subprocess.run(cmd, shell=True)


###################################################### dxf to shape

# data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")

# data['geom_type']= data.geometry.type

# # split lines and points
# data_lines = data.loc[data.geom_type == 'LineString']
# data_points = data.loc[data.geom_type == 'Point']

# # export the data to shapefiles
# data_lines.to_file("./output/lines.shp")
# data_points.to_file("./output/points.shp")

#####################################################

# import geopandas as gpd
# from shapely.geometry import box

# # Read the DXF file into a GeoDataFrame
# # data = gpd.read_file("./output/Plan & Profile KM 0-5.dxf")
# data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")

# # Add a new column for geometry type
# data['geom_type'] = data.geometry.type

# # Calculate the bounding box of all features in the GeoDataFrame
# bounding_box = data.total_bounds  # Returns (minx, miny, maxx, maxy)
# min_x, min_y, max_x, max_y = bounding_box
# print(f"Bounding Box: {bounding_box}")

# # Create a bounding box polygon
# # bounding_box_polygon = box(min_x, min_y, max_x, max_y)
# # bounding_box_polygon = box(0, min_y, 21000, max_y)
# bounding_box_polygon = box(637000, 3902000, 672000, 3919000)

# # Select features within the bounding box
# cropped_data = data[data.geometry.intersects(bounding_box_polygon)]

# # Split cropped data into lines and points
# data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
# data_points = cropped_data[cropped_data['geom_type'] == 'Point']

# # Export the cropped LineString geometries to a shapefile
# data_lines.to_file("./output/cropped_lines.shp")

# # Export the cropped Point geometries to a shapefile
# data_points.to_file("./output/cropped_points.shp")

# print("Cropped data conversion completed!")

#############################################################
import geopandas as gpd
from shapely.geometry import box

# Read the DXF file into a GeoDataFrame
# data = gpd.read_file("./output/Plan & Profile KM 0-5.dxf")
data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")

# Add a new column for geometry type
data['geom_type'] = data.geometry.type

# Set the CRS for the GeoDataFrame (example: EPSG:4326 for WGS84)
data.set_crs(epsg=4326, inplace=True)

# Calculate the bounding box of all features in the GeoDataFrame
bounding_box = data.total_bounds  # Returns (minx, miny, maxx, maxy)
min_x, min_y, max_x, max_y = bounding_box
print(f"Bounding Box: {bounding_box}")

# Create a bounding box polygon
# bounding_box_polygon = box(min_x, min_y, max_x, max_y)
# bounding_box_polygon = box(0, min_y, 21000, max_y)
bounding_box_polygon = box(637000, 3902000, 672000, 3919000)

# Select features within the bounding box
cropped_data = data[data.geometry.intersects(bounding_box_polygon)]

# Split cropped data into lines and points
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']

# Export the cropped LineString geometries to a shapefile
data_lines.to_file("./output/cropped_lines.shp")

# Export the cropped Point geometries to a shapefile
data_points.to_file("./output/cropped_points.shp")

print("Cropped data conversion completed!")






