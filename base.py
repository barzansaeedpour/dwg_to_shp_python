import subprocess
import geopandas as gpd
from shapely.geometry import box
from shapely.affinity import translate

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
bounding_box_polygon = box(637000, 3902000, 672000, 3919000)
cropped_data = data[data.geometry.intersects(bounding_box_polygon)]

# Translate the cropped data to the new center coordinates (5715364, 4261022)
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']

current_center_x, current_center_y = (bounding_box[0] + bounding_box[2]) / 2, (bounding_box[1] + bounding_box[3]) / 2
new_center_x, new_center_y = 5715364, 4261022
delta_x, delta_y = new_center_x - current_center_x, new_center_y - current_center_y

data_lines['geometry'] = data_lines['geometry'].apply(lambda geom: translate(geom, xoff=delta_x, yoff=delta_y))
data_points['geometry'] = data_points['geometry'].apply(lambda geom: translate(geom, xoff=delta_x, yoff=delta_y))

# Save the shapefiles
data_lines.to_file("./output/cropped_lines_translated.shp")
data_points.to_file("./output/cropped_points_translated.shp")

print("Cropped data translation completed!")
