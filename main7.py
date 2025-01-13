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
bounding_box_polygon = box(637000, 3902000, 672000, 3919000)
cropped_data = data[data.geometry.intersects(bounding_box_polygon)]
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']

# Calculate the translation distance
current_center_x, current_center_y = bounding_box[0] + (bounding_box[2] - bounding_box[0]) / 2, bounding_box[1] + (bounding_box[3] - bounding_box[1]) / 2
new_center_x, new_center_y = 5715364, 4261022
delta_x, delta_y = new_center_x - current_center_x, new_center_y - current_center_y

# Translate the geometries
data_lines['geometry'] = data_lines['geometry'].apply(lambda geom: translate(geom, xoff=delta_x, yoff=delta_y))
data_points['geometry'] = data_points['geometry'].apply(lambda geom: translate(geom, xoff=delta_x, yoff=delta_y))

# Scale the geometries (scale factor example: 1.5 for zooming in, 0.5 for zooming out)
scale_factor = 4
data_lines['geometry'] = data_lines['geometry'].apply(lambda geom: scale(geom, xfact=scale_factor, yfact=scale_factor, origin='centroid'))
data_points['geometry'] = data_points['geometry'].apply(lambda geom: scale(geom, xfact=scale_factor, yfact=scale_factor, origin='centroid'))

# Save the shapefiles
data_lines.to_file("./output/cropped_lines_scaled_4.shp")
data_points.to_file("./output/cropped_points_scaled_4.shp")

print("Cropped data translation and scaling completed!")
