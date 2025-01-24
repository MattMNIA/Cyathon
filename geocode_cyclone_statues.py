import csv
from geopy.geocoders import Nominatim
from time import sleep

# Initialize the geolocator
geolocator = Nominatim(user_agent="cyclone_city_geocoder")

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
        if address:
            lat, long = get_lat_long(address)
            sleep(1)  # Pause to avoid overwhelming the geocoding service
        else:
            lat, long = None, None

        # Write the new row with latitude and longitude
        writer.writerow([id_, name, location, address, lat, long])

print("Geocoding complete. Check the output CSV for results.")
