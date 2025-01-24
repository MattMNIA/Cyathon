import csv
import networkx as nx
import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer
import math
import matplotlib.colors as mcolors

def create_graph_from_csv(csv_file):
    G = nx.Graph()
    
    # Read the CSV file and add nodes
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            statue_id = row[0]
            lat = float(row[4])  # latitude
            lon = float(row[5])  # longitude
            G.add_node(statue_id, lat=lat, lon=lon)
    
    return G

def add_edge(G, node1, node2, weight):
    G.add_edge(node1, node2, weight=weight)

def draw_graph(nx_graph, path=None):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
    pos = {}
    for n in nx_graph.nodes():
        lat, lon = nx_graph.nodes[n]['lat'], nx_graph.nodes[n]['lon']
        x, y = transformer.transform(lon, lat)
        pos[n] = (x, y)
    
    fig, axes = plt.subplots(1,1,dpi=70)
    
    # Draw all edges in gray first
    nx.draw_networkx_edges(nx_graph, pos, ax=axes, edge_color='gray', width=5)
    
    if path:
        # Create edge list from path
        path_edges = list(zip(path[:-1], path[1:]))
        # Draw path edges in red
        nx.draw_networkx_edges(nx_graph, pos, ax=axes, edgelist=path_edges, 
                             edge_color='red', width=2)
    
    # Draw nodes and labels
    nx.draw_networkx_nodes(nx_graph, pos, ax=axes, node_color='lightblue')
    nx.draw_networkx_labels(nx_graph, pos, ax=axes)
    
    ctx.add_basemap(axes, crs="EPSG:3857",
                   source=ctx.providers.OpenStreetMap.Mapnik,
                   zoom=14)
    plt.show()

def find_distance(lat1, lon1, lat2, lon2):
    R = 3963.1  # Radius of the Earth in miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def find_closest_neighbors_num(graph, node_id, num_neighbors=3):
    closest_neighbors = []
    node_data = graph.nodes[node_id]
    for other_id in graph.nodes():
        if other_id != node_id:
            other_data = graph.nodes[other_id]
            distance = find_distance(
                node_data['lat'], node_data['lon'],
                other_data['lat'], other_data['lon']
            )
            closest_neighbors.append((other_id, distance))
    if len(closest_neighbors) > 3:
        closest_neighbors.sort(key=lambda x: x[1])
        closest_neighbors = closest_neighbors[:num_neighbors]
    return closest_neighbors

def add_edges_between_nearest(graph, num_neighbors):
    for node_id in graph.nodes():
        closest_neighbors = find_closest_neighbors_num(graph, node_id,num_neighbors)
        for neighbor_id, distance in closest_neighbors:
            add_edge(graph, node_id, neighbor_id, distance)

# Example usage
if __name__ == "__main__":
    graph = create_graph_from_csv("final_cyclone_city_statues_with_coordinates.csv")
    
    # Add edges to the graph based on closest neighbors
    for node_id in graph.nodes():
        closest_neighbors = find_closest_neighbors_num(graph, node_id,3)
        for neighbor_id, distance in closest_neighbors:
            add_edge(graph, node_id, neighbor_id, distance)
    
    # Print the edges with weights
    print(graph.edges(data=True))
    
    # Draw graph
    draw_graph(graph)
