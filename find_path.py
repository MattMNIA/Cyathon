import networkx as nx
import create_graph as cg

def approx_tsp(G):
    # Use NetworkX's built-in approximate TSP solver
    tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)
    tsp_cost = sum(G[tsp_path[i]][tsp_path[i + 1]]['weight'] for i in range(len(tsp_path) - 1))

    print(f"Approximate TSP Path: {tsp_path}")
    print(f"Approximate TSP Cost: {tsp_cost}")
    return tsp_cost, tsp_path

def find_path_with_cost(graph, start, target_cost, tolerance=0.1):
    """
    Find a path in the graph whose total cost is approximately the target cost.

    Parameters:
        graph: NetworkX graph with edge weights.
        start: Starting node.
        target_cost: Desired total cost of the path.
        tolerance: Allowable deviation from the target cost.

    Returns:
        The path and its cost, or None if no such path exists.
    """
    def dfs(node, visited, current_cost, path):
        # Base case: Check if we're close enough to the target cost
        if abs(current_cost - target_cost) <= tolerance:
            return path, current_cost
        
        # Explore neighbors
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                edge_cost = graph[node][neighbor]['weight']
                if current_cost + edge_cost <= target_cost + tolerance:  # Prune paths that exceed the cost
                    visited.add(neighbor)
                    result = dfs(neighbor, visited, current_cost + edge_cost, path + [neighbor])
                    if result:  # Found a valid path
                        return result
                    visited.remove(neighbor)  # Backtrack
        
        return None

    # Start DFS
    visited = set([start])
    return dfs(start, visited, 0, [start])

G = cg.create_graph_from_csv("final_cyclone_city_statues_with_coordinates.csv")
cg.add_edges_between_nearest(G, 5)

start_node = "16"
target_cost = 26.2
path, cost = find_path_with_cost(G, start_node, target_cost)
if path:
    print(f"Path found: {path} with cost: {cost}")
else:
    print("No path found with the desired cost.")
cg.draw_graph(G, path)



# G = cg.create_graph_from_csv("final_cyclone_city_statues_with_coordinates.csv")
# cg.add_edges_between_nearest(G, 10)
# min_cost, path = approx_tsp(G)

# cg.draw_graph(G, path)
