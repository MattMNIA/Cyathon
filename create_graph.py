import csv
import networkx as nx
import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer

def create_graph_from_csv(csv_file):
    G = nx.Graph()
    
    # Read the CSV file and add nodes
    with open(csv_file, 'r') as file:
        print("reading")
        reader = csv.reader(file)
        for row in reader:
            statue_id = row[0]
            lat = float(row[4])  # latitude
            lon = float(row[5])  # longitude
            G.add_node(statue_id, lat=lat, lon=lon)
    
    return G

def add_edge(G, node1, node2, weight):
    G.add_edge(node1, node2, weight=weight)

def draw_graph(nx_graph):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
    pos = {}
    for n in nx_graph.nodes():
        lat, lon = nx_graph.nodes[n]['lat'], nx_graph.nodes[n]['lon']
        x, y = transformer.transform(lon, lat)
        pos[n] = (x, y)
    fig, axes = plt.subplots(1,1,dpi=72)
    nx.draw(nx_graph, pos=pos, ax=axes, with_labels=True)
    ctx.add_basemap(axes, crs="EPSG:3857")
    plt.show()
    
# Example usage
if __name__ == "__main__":
    graph = create_graph_from_csv("cyclone_city_statues_with_coordinates.csv")
    
    # Add edges with weights
    add_edge(graph, '1', '2', 10)
    add_edge(graph, '2', '3', 5)
    
    # Print the edges with weights
    print(graph.edges(data=True))
    
    # Draw graph
    draw_graph(graph)
