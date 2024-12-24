import subprocess
import geopandas as gpd


##################################### dwg to dxf
# INPUT_FOLDER = "./input/"
# OUTPUT_FOLDER = "./output"


# TEIGHA_PATH = "C:/Program Files/ODA/ODAFileConverter 25.11.0/ODAFileConverter.exe"
# OUTVER = "ACAD2018"
# OUTFORMAT = "DXF"
# RECURSIVE = "0"
# AUDIT = "1"
# INPUTFILTER = "*.DWG"

# # Command to run
# cmd = [TEIGHA_PATH, INPUT_FOLDER, OUTPUT_FOLDER, OUTVER, OUTFORMAT, RECURSIVE, AUDIT, INPUTFILTER]

# # Run
# subprocess.run(cmd, shell=True)


##################################### dxf to shape

data = gpd.read_file("./output/Khoroseh Var-Plan & Profile.dxf")

data['geom_type']= data.geometry.type

# split lines and points
data_lines = data.loc[data.geom_type == 'LineString']
data_points = data.loc[data.geom_type == 'Point']

# export the data to shapefiles
data_lines.to_file("./output/lines.shp")
data_points.to_file("./output/points.shp")





