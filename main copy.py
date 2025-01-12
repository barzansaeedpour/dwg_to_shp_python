import subprocess
import geopandas as gpd
import geopandas as gpd
from shapely.geometry import box


INPUT_FOLDER = "./input/"
OUTPUT_FOLDER = "./output"
TEIGHA_PATH = "C:/Program Files/ODA/ODAFileConverter 25.11.0/ODAFileConverter.exe"
OUTVER = "ACAD2018"
OUTFORMAT = "DXF"
RECURSIVE = "0"
AUDIT = "1"
INPUTFILTER = "*.DWG"
cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]
subprocess.run(cmd, shell=True)
data = gpd.read_file("./output/file.dxf")
data['geom_type'] = data.geometry.type
data.set_crs(epsg=4326, inplace=True)
bounding_box = data.total_bounds  # Returns (minx, miny, maxx, maxy)
min_x, min_y, max_x, max_y = bounding_box
print(f"Bounding Box: {bounding_box}")
bounding_box_polygon = box(637000, 3902000, 672000, 3919000)
cropped_data = data[data.geometry.intersects(bounding_box_polygon)]
data_lines = cropped_data[cropped_data['geom_type'] == 'LineString']
data_points = cropped_data[cropped_data['geom_type'] == 'Point']
data_lines.to_file("./output/cropped_lines.shp")
data_points.to_file("./output/cropped_points.shp")
print("Cropped data conversion completed!")






