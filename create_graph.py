import csv
import networkx as nx

def create_graph_from_csv(csv_file):
    G = nx.Graph()
    
    # Read the CSV file and add nodes
    with open(csv_file, 'r') as file:
        print("reading")
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            statue_id = row[0]
            G.add_node(statue_id)
    
    return G

def add_edge(G, node1, node2, weight):
    G.add_edge(node1, node2, weight=weight)

# Example usage
if __name__ == "__main__":
    graph = create_graph_from_csv("cyclone_city_statues.csv")
    
    # Add edges with weights
    add_edge(graph, 'statue1', 'statue2', 10)
    add_edge(graph, 'statue2', 'statue3', 5)
    
    # Print the edges with weights
    print(graph.edges(data=True))
