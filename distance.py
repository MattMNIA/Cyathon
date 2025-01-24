import csv
import osmnx as ox
import networkx as nx

def calculate_walking_distance_osmnx(origin_coords, destination_coords):
    # Get the graph of the area
    graph = ox.graph_from_point(origin_coords, dist=1000, network_type='walk')

    # Find the nearest nodes in the graph to the origin and destination
    origin_node = ox.distance.nearest_nodes(graph, origin_coords[1], origin_coords[0])
    destination_node = ox.distance.nearest_nodes(graph, destination_coords[1], destination_coords[0])

    # Calculate the shortest path length
    distance = nx.shortest_path_length(graph, origin_node, destination_node, weight='length')
    return distance

input_csv = r"C:\Users\mattc\Box\Personal Projects\Cyathon\cyclone_city_statues_with_coordinates.csv"
output_csv = r"C:\Users\mattc\Box\Personal Projects\Cyathon\cyclone_city_statues_with_coordinates_dist_from_apt.csv"
origin_coords = (42.022664, -93.660473)


with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    for row in reader:
            id_, name, location, address, long, lat = row

            destination_coords = (float(long), float(lat))
            distance = calculate_walking_distance_osmnx(origin_coords, destination_coords)
            writer = csv.writer(outfile)
            writer.writerow([id_, name, location, address, long, lat, distance])



