#Import the packages 
import networkx as nx # networkx package 
import osmnx as ox 
import pandas as pd #Base package for data analysis and manipulation 
import geopandas as gpd #A more flexible package to work with geospatial data in python 
import shapely.geometry #python package for basic spatial operation 
from osgeo import ogr #GDAL package 
from pyproj import CRS #package for your projection management 

from pathlib import Path #Path modification package 
import os #operating system package 

import matplotlib.pyplot as plt #package for plotting 

#configure in notebook 
#%matplotlib inline  
#print the version 
ox.__version__ 

#Setting the directory 
#Check current working directory 
os.getcwd() 

#Change to the folder you are working  (maybe dubbel slash if not working)
Path = 'C:\\Users\\rensw\\OneDrive - Universiteit Utrecht\\GIMA\\Module 6\\Python code\\OSMnx\\Labib Code' 
#change based on you PC’s set up 

os.chdir (Path) 

#Check new directory 
os.getcwd() 

# input point of origin and point of destination
origLatPoint = 52.373186 
origLngPoint = 4.891368
destLatPoint = 52.3471806
destLngPoint = 4.9185823

#set the city names
g_namen = ['Amsterdam', 'Rotterdam', "Den_Haag", "Utrecht"]

#download city geometries from file
project_gemeenten = gpd.read_file(r"data\UrbanRunner_Areas.geojson")

#set index to gemeentenaam column
project_gemeenten.set_index('gemeentenaam', inplace=True)

#project to WGS84
project_gemeenten.to_crs("EPSG:4326", inplace=True)

#set additional geometry column of convex hull
project_gemeenten["convexhull"] = project_gemeenten.convex_hull

#Download city network graphs
for gemeente in g_namen:
    globals()[f"{gemeente}_polygon"] = project_gemeenten.loc[gemeente].geometry.convex_hull
    globals()[f"{gemeente}_network"] = ox.graph_from_polygon(globals()[f"{gemeente}_polygon"], network_type="walk")

##G = ox.project_graph(place, to_crs='epsg:28992')
##fig, ax = ox.plot_graph(G, node_size=0)

#Find area of network
G_proj = ox.project_graph(G) 
nodes_proj = ox.graph_to_gdfs(G_proj, edges=False) 
graph_area_m = nodes_proj.unary_union.convex_hull.area 
graph_area_m 

# Retrieve only edges from the graph 
nodes_proj, edges = ox.graph_to_gdfs(G, nodes=True, edges=True) 

#print the edge table 
edges 

#Get the bounding box of all the edges, this will be the are of interest for each city 
#convex_hull = edges.unary_union.convex_hull 
bbox_env = edges.unary_union.envelope 
bbox_env 

# show some basic stats about the network
ox.basic_stats(G, area=place, clean_int_tol=True, circuity_dist="euclidean")

## convert your MultiDiGraph to an undirected MultiGraph
M = ox.get_undirected(G)

# impute missing edge speeds then calculate edge travel times
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# get the nearest network nodes to two lat/lng points
orig = ox.distance.nearest_nodes(G, origLatPoint, origLngPoint, return_dist=False)
dest = ox.distance.nearest_nodes(G, destLatPoint, destLngPoint, return_dist=False)

# find the shortest path between these nodes, minimizing travel time, then plot it
route = ox.shortest_path(G, orig, dest, weight="travel_time")
fig, ax = ox.plot_graph_route(G, route, node_size=0)

# how long is our route in meters?
edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
sum(edge_lengths)

# how far is it between these two nodes as the crow flies (haversine)?
ox.distance.great_circle_vec(
    G.nodes[orig]["y"], G.nodes[orig]["x"], G.nodes[dest]["y"], G.nodes[dest]["x"]
)

# add elevation to nodes automatically, calculate edge grades, plot network
# you need a google elevation api key to run this cell!
try:
    from keys import google_elevation_api_key

    G = ox.add_node_elevations(G, api_key=google_elevation_api_key)
    G = ox.add_edge_grades(G)
    nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
    fig, ax = ox.plot_graph(G, node_color=nc, node_size=20, edge_linewidth=2, edge_color="#333")
except ImportError:
    pass

# get all drinking water taps in neighborhood
tags = {"amenity=drinking_water":True}
gdf = ox.geometries_from_place(G, tags)
gdf.shape

watertap_amenities = ox.geometries_from_place(G, tags={"amenity": "drinking_water"})
watertap_amenities.explore()

# Now convert it to a shapefile with OGR    [Copied from one post in Stake Exchange] 
driver = ogr.GetDriverByName('ESRI Shapefile') #for ESRI shapefile 
ds = driver.CreateDataSource('citybound.shp') #Name of the file  
layer = ds.CreateLayer('', None, ogr.wkbPolygon) 

# Add one attribute 
layer.CreateField(ogr.FieldDefn('id', ogr.OFTString)) 
defn = layer.GetLayerDefn() 

# Create a new feature (attribute and geometry) 
feat = ogr.Feature(defn) 
feat.SetField('id', name) 

# Make a geometry, from Shapely object 
# geom = ogr.CreateGeometryFromWkb(poly.wkb) 
# feat.SetGeometry(geom) 

#layer.CreateFeature(feat) 
#feat = geom = None  

# Save graph to disk as geopackage (for GIS) or graphml file (for gephi etc) and close
ds = layer = feat = geom = None 
ox.save_graph_geopackage(G, filepath="./data/mynetwork.gpkg") 
ox.save_graphml(G, filepath="./data/mynetwork.graphml")
