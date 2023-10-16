import geopandas as gpd

# Read the GPKG file
gdf = gpd.read_file('Boundaries\State.gpkg')

# Write the GeoDataFrame to a GEOJSON file
gdf.to_file('Boundaries\State.geojson', driver='GeoJSON')

