import subprocess
import geopandas as gpd
from shapely.geometry import box
from shapely.affinity import translate, scale

# Constants for file paths and configurations
INPUT_FOLDER = "./input/"
OUTPUT_FOLDER = "./output"
TEIGHA_PATH = "C:/Program Files/ODA/ODAFileConverter 25.11.0/ODAFileConverter.exe"
OUTVER = "ACAD2018"
OUTFORMAT = "DXF"
RECURSIVE = "0"
AUDIT = "1"
INPUTFILTER = "*.DWG"

# Convert DWG to DXF using ODA File Converter
cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]
subprocess.run(cmd, shell=True)

# Load the converted DXF file using GeoPandas
data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")
data['geom_type'] = data.geometry.type
data.set_crs(epsg=3857, inplace=True)

# Calculate the bounding box and crop the data
bounding_box = data.total_bounds  # Returns (minx, miny, maxx, maxy)
print(f"Bounding Box: {bounding_box}")

# Define new bounding box coordinates for zooming in or out
zoom_factor = -0.5  # Adjust this factor to zoom in or out. >1 for zooming out, <1 for zooming in
min_x, min_y, max_x, max_y = bounding_box
center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2
new_min_x = center_x - (center_x - min_x) * zoom_factor
new_max_x = center_x + (max_x - center_x) * zoom_factor
new_min_y = center_y - (center_y - min_y) * zoom_factor
new_max_y = center_y + (max_y - center_y) * zoom_factor

bounding_box_polygon = box(new_min_x, new_min_y, new_max_x, new_max_y)
cropped_data = data[data.geometry.intersects(bounding_box_polygon)]

# Translate the cropped data to the new center coordinates (5715364, 4261022)
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']

current_center_x, current_center_y = (new_min_x + new_max_x) / 2, (new_min_y + new_max_y) / 2
new_center_x, new_center_y = 5715364, 4261022
delta_x, delta_y = new_center_x - current_center_x, new_center_y - current_center_y

data_lines['geometry'] = data_lines['geometry'].apply(lambda geom: translate(geom, xoff=delta_x, yoff=delta_y))
data_points['geometry'] = data_points['geometry'].apply(lambda geom: translate(geom, xoff=delta_x, yoff=delta_y))

# Save the shapefiles
data_lines.to_file("./output/cropped_lines_zoomed.shp")
data_points.to_file("./output/cropped_points_zoomed.shp")

print("Cropped data translation and zooming completed!")
