"""
getting network extent from UrbanRunner_Areas dataset
"""

#set the city names
g_namen = ['Amsterdam', 'Rotterdam', "Den_Haag", "Utrecht"]

#download city geometries from file
project_gemeenten = gpd.read_file(r"data\UrbanRunner_Areas.geojson")

#set additional geometry column of extent
project_gemeenten["extent"] = project_gemeenten.envelope.buffer(2000).to_crs("EPSG:4326")

#set index to gemeentenaam column
project_gemeenten.set_index('gemeentenaam', inplace=True)

#project to WGS84
project_gemeenten.to_crs("EPSG:4326", inplace=True)
project_gemeenten['extent'].to_crs("EPSG:4326")


"""
get the names of the AHN_tiles per area, and then download the AHN DTM_05M_DTM for these tiles.
"""
#get the downloadtiles of AHN4 and reproject to WGS84
ahn_datavlakken = gpd.read_file(r"data/kaartbladen_AHN4.gpkg")
ahn_datavlakken.to_crs("EPSG:4326", inplace=True)

#get the area specific tiles with clipping function
for g in g_namen:
    globals()[f"{g}_ahnvlakken"]=ahn_datavlakken.clip(project_gemeenten.loc[g].extent.envelope)

#download the DTM from the tiles
for g in g_namen:
    for i in range(globals()[f"{g}_ahnvlakken"].Name_1.count()):    
        name = globals()[f"{g}_ahnvlakken"].iat[i,2]
        response = requests.get(globals()[f"{gemeente}_ahnvlakken"].iat[i,3])
        print('done with downloading tile', name,  'of gemeente', g)
        open('data\\AHN4_05M_DTM\\'+gemeente + '\\'+ name + '.zip', "wb").write(response.content)
