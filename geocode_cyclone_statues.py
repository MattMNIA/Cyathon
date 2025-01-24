import csv
from geopy.geocoders import Nominatim
from time import sleep

# Initialize the geolocator
geolocator = Nominatim(user_agent="cyclone_city_geocoder")
loc = Nominatim(user_agent="Geopy Library")

# Read the CSV file
input_csv = './cyclone_city_statues.csv'
output_csv = './cyclone_city_statues_with_coordinates.csv'

# Define a function to get latitude and longitude
def get_lat_long(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            print(f"Geocoded {address} successfully")
            return location.latitude, location.longitude
        else:
            print(f"Geocoded {address} UNSUCCESSFULLY")

        return None, None
    except Exception as e:
        print(f"Error fetching coordinates for {address}: {e}")
        return None, None

# Open the input and output CSV files
with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read each row and append coordinates
    for row in reader:
        id_, name, location, address = row
        print(id_, address)
        if address:
            if id_ == '13':
                print("IN ID 13")
                lat, long = 42.026861,-93.652451
            else:
                lat, long = get_lat_long(address)
                sleep(1)  # Pause to avoid overwhelming the geocoding service
        elif id_ == '17':
            lat, long = 42.012313,-93.635931
        else:
            lat, long = None, None

        # Write the new row with latitude and longitude
        writer.writerow([id_, name, location, address, lat, long])

print("Geocoding complete. Check the output CSV for results.")
