from daftlistings import Daft, Location, SearchType, PropertyType
from pprint import pprint
from flask import Flask, request, jsonify
import math    

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Create an instance of the Daft class
daft = Daft()

#test = calculate_distance(53.4040944, -6.2946463, 53.30323370042453, -6.256870048826886)
#print(test)

daft.set_location(Location.DUBLIN)
daft.set_search_type(SearchType.RESIDENTIAL_SALE)
# Call the search method on the Daft instance with the updated parameters
listings = daft.search()

target_latitude = 53.30323370042453
target_longitude = -6.256870048826886
max_distance = 0.5

nearby_listings = []
for listing in listings:
    distance = calculate_distance(listing.latitude, listing.longitude, target_latitude, target_longitude)
    if distance <= max_distance:
        nearby_listings.append(listing)

for listing in nearby_listings:
    
    print(listing)

