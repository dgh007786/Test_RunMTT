import geopandas as gpd
import random

# Load the shapefile
input_path = "/home/gunjan/Desktop/Test_RunMTT/test_cases/case1/Ignition.shp"
gdf = gpd.read_file(input_path)

# Check how many points you have
print(f"Original count: {len(gdf)}")

# Sample 500 random points (without replacement)
sampled_gdf = gdf.sample(n=500, random_state=42)

# Save to a new shapefile
output_path = "/home/gunjan/Desktop/Test_RunMTT/test_cases/case1/Ignition_small.shp"
sampled_gdf.to_file(output_path)

print(f"Sample saved to: {output_path}")
