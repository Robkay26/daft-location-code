from daftlistings import Daft, Location, SearchType, PropertyType
from pprint import pprint
from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/coordinates', methods=['POST'])
def process_coordinates():
    try:
        data = request.json
        print(data)
        lat = data['coordinates']['lat']
        lng = data['coordinates']['lng']
        print(lat, lng)

        nearby_houses = find_nearby_houses(lat, lng)

        return jsonify({'nearby_houses': nearby_houses}), 200
    except Exception as e:
        return jsonify({'error python': str(e)}), 500


def find_nearby_houses(target_latitude, target_longitude):
    
    daft = Daft()
    #daft.set_location([Location.DUBLIN_14_DUBLIN, Location.DUBLIN_6_DUBLIN])
    daft.set_search_type(SearchType.RESIDENTIAL_SALE)

    listings = daft.search()

    max_distance = 1

    nearby_listings = []
    for listing in listings:
        distance = calculate_distance(listing.latitude, listing.longitude, target_latitude, target_longitude)
        if distance <= max_distance:
            nearby_listings.append({
                'title': listing.title,
                'latitude': listing.latitude,
                'longitude': listing.longitude,
                'link' : listing.daft_link
            })

    return nearby_listings     
    
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

if __name__ == "__main__":
    app.run(port=8080)