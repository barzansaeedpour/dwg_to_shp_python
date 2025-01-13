import subprocess
import geopandas as gpd
from shapely.geometry import box
import folium

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
cropped_data = data
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']

# Save the shapefiles
data_lines.to_file("./output/cropped_lines.shp")
data_points.to_file("./output/cropped_points.shp")

# Create a map centered on the new coordinates (5715364, 4261022)
new_center_lat = 4261022
new_center_long = 5715364
m = folium.Map(location=[new_center_lat, new_center_long], zoom_start=12, crs='EPSG3857')

# Add cropped lines and points to the map
folium.GeoJson(data_lines).add_to(m)
folium.GeoJson(data_points).add_to(m)

# Save the map as an HTML file
m.save("./output/map.html")

print("Map centered on new coordinates created and saved as map.html!")
