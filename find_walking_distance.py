import osmnx as ox
import networkx as nx
from haversine import haversine
import csv
import time

def get_nodes(csv_file):
    nodes = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            statue_id = row[0]
            lat = float(row[4])  # latitude
            lon = float(row[5])  # longitude
            nodes[statue_id] = (lat, lon)
    return nodes

def get_walking_graph(nodes):
    # Get the walking network around the nodes
    locations = list(nodes.values())
    center = (sum(lat for lat, lon in locations) / len(locations),
            sum(lon for lat, lon in locations) / len(locations))
    # Set a reasonable buffer distance for the walking network
    walking_graph = ox.graph_from_point(center, dist=10000, network_type='walk')

    return walking_graph

def calculate_walking_distances(nodes, walking_graph):
    """
    Calculate walking distances between all pairs of nodes.

    Parameters:
        nodes: Dictionary of node IDs and their (lat, lon).
        walking_graph: The OSMnx graph for walking.

    Returns:
        A NetworkX weighted graph with walking distances.
    """
    print(f"Starting calculations for {len(nodes)} nodes...")
    total_pairs = len(nodes) * (len(nodes) - 1) // 2
    print(f"Total pairs to process: {total_pairs}")
    start_time = time.time()
    processed = 0
    G = nx.Graph()
    
    for node1, (lat1, lon1) in nodes.items():
        for node2, (lat2, lon2) in nodes.items():
            if node1 != node2:
                processed += 1
                if processed % 10 == 0:  # Update every 10 pairs
                    elapsed = time.time() - start_time
                    rate = processed / elapsed if elapsed > 0 else 0
                    remaining_pairs = max(0, total_pairs - processed)
                    estimated_remaining_time = remaining_pairs / rate if rate > 0 else float('inf')
                    print(f"Processed {processed}/{total_pairs} pairs. "
                          f"Estimated time remaining: {max(0, estimated_remaining_time/60):.1f} minutes")

                # Find the nearest OSMnx nodes to our coordinates
                osm_node1 = ox.distance.nearest_nodes(walking_graph, lon1, lat1)
                osm_node2 = ox.distance.nearest_nodes(walking_graph, lon2, lat2)
                
                # Calculate the shortest walking distance between them
                try:
                    distance = nx.shortest_path_length(
                        walking_graph, source=osm_node1, target=osm_node2, weight='length'
                    )
                except nx.NetworkXNoPath:
                    distance = float('inf')  # No walking path found
                
                G.add_edge(node1, node2, weight=distance)
    
    total_time = time.time() - start_time
    print(f"\nCalculations complete! Total time: {total_time/60:.1f} minutes")
    return G

nodes = get_nodes("final_cyclone_city_statues_with_coordinates.csv")
walking_graph = get_walking_graph(nodes)
# Generate the new graph with walking distances
walking_distance_graph = calculate_walking_distances(nodes, walking_graph)
print(walking_distance_graph)
# Plot the original walking graph instead of the distance graph
ox.plot_graph(walking_graph)

# If you want to see the actual distances, you can print them:
for (node1, node2, weight) in walking_distance_graph.edges(data='weight'):
    print(f"Distance between {node1} and {node2}: {weight:.2f} meters")


