# Boilerplate for AI Assignment — Knowledge Representation, Reasoning and Planning
# CSE 643

# Import necessary libraries
import heapq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
from pyDatalog import pyDatalog
from collections import Counter, defaultdict, deque


## ****IMPORTANT****
## Don't import or use any other libraries other than defined above
## Otherwise your code file will be rejected in the automated testing

# ------------------ Global Variables ------------------
route_to_stops = defaultdict(list)  # Mapping of route IDs to lists of stops
trip_to_route = {}                   # Mapping of trip IDs to route IDs
stop_trip_count = defaultdict(int)    # Count of trips for each stop
fare_rules = {}                      # Mapping of route IDs to fare information
merged_fare_df = None                # To be initialized in create_kb()

# Load static data from GTFS (General Transit Feed Specification) files
df_stops = pd.read_csv('./GTFS/stops.txt')
df_routes = pd.read_csv('./GTFS/routes.txt')
df_stop_times = pd.read_csv('./GTFS/stop_times.txt')
df_fare_attributes = pd.read_csv('./GTFS/fare_attributes.txt')
df_trips = pd.read_csv('./GTFS/trips.txt')
df_fare_rules = pd.read_csv('./GTFS/fare_rules.txt')

# ------------------ Function Definitions ------------------

# Function to create knowledge base from the loaded data
def create_kb():
    """
    Create knowledge base by populating global variables with information from loaded datasets.
    It establishes the relationships between routes, trips, stops, and fare rules.
    
    Returns:
        None
    """
    global route_to_stops, trip_to_route, stop_trip_count, fare_rules, merged_fare_df

    # Create trip_id to r_id mapping
    trip_to_route = {rps['trip_id']: rps['route_id'] for rps in df_trips.to_dict('records')}

    for rps in df_stop_times.to_dict('records'):
        route_id = trip_to_route[rps['trip_id']]
        stop_id = rps['stop_id']

        route_to_stops.setdefault(route_id, []).append(stop_id)
        fare_rules.setdefault(stop_id, []).append(route_id)
        stop_trip_count[stop_id] = stop_trip_count.get(stop_id, 0) + 1

    for r_id in route_to_stops:
        route_to_stops[r_id] = sorted(set(route_to_stops[r_id]))
        fare_rules[r_id] = sorted(set(fare_rules.get(r_id, [])))
        
    
# Function to find the top 5 busiest routes based on the number of trips
def get_busiest_routes():
    """
    Identify the top 5 busiest routes based on trip counts.

    Returns:
        list: A list of tuples, where each tuple contains:
              - route_id (int): The ID of the route.
              - trip_count (int): The number of trips for that route.
    """
    return Counter(trip_to_route.values()).most_common(5)


# Function to find the top 5 stops with the most frequent trips
def get_most_frequent_stops():
    """
    Identify the top 5 stops with the highest number of trips.

    Returns:
        list: A list of tuples, where each tuple contains:
              - stop_id (int): The ID of the stop.
              - trip_count (int): The number of trips for that stop.
    """
    return Counter(stop_trip_count).most_common(5)

# Function to find the top 5 busiest stops based on the number of routes passing through them
def get_top_5_busiest_stops():
    """
    Identify the top 5 stops with the highest number of different routes.

    Returns:
        list: A list of tuples, where each tuple contains:
              - stop_id (int): The ID of the stop.
              - route_count (int): The number of routes passing through that stop.
    """
    route_counts = Counter()
    for rts in route_to_stops.values():
        route_counts.update(rts)

    return route_counts.most_common(5)

# Function to identify the top 5 pairs of stops with only one direct route between them
def get_stops_with_one_direct_route():
    """
    Identify the top 5 pairs of consecutive stops (start and end) connected by exactly one direct route. 
    The pairs are sorted by the combined frequency of trips passing through both stops.

    Returns:
        list: A list of tuples, where each tuple contains:
              - pair (tuple): A tuple with two stop IDs (stop_1, stop_2).
              - route_id (int): The ID of the route connecting the two stops.
    """

    stop_pair_data = defaultdict(lambda: {'routes': set(), 'trips': 0})

    for r_id, stp in route_to_stops.items():
        for i in range(len(stp) - 1):
            start, end = stp[i], stp[i + 1]
            pair = (start, end)
            stop_pair_data[pair]['routes'].add(r_id)
            stop_pair_data[pair]['trips'] += stop_trip_count[start] + stop_trip_count[end]

    single_route_pairs = [(pair, next(iter(data['routes']))) 
                         for pair, data in stop_pair_data.items() 
                         if len(data['routes']) == 1]

    return sorted(single_route_pairs, key=lambda x: stop_pair_data[x[0]]['trips'], reverse=True)[:5]

# Function to get merged fare DataFrame
# No need to change this function
def get_merged_fare_df():
    """
    Retrieve the merged fare DataFrame.

    Returns:
        DataFrame: The merged fare DataFrame containing fare rules and attributes.
    """
    global merged_fare_df
    if merged_fare_df is None:
        create_kb()
        merged_fare_df = (
            pd.merge(df_fare_rules, df_fare_attributes, on="fare_id")
            .drop_duplicates(subset='fare_id', keep='first')
            .sort_values(by='fare_id')
            .reset_index(drop=True)
        )
    return merged_fare_df

# Visualize the stop-route graph interactively
def visualize_stop_route_graph_interactive(route_to_stops):
    """
    Visualize the stop-route graph using Plotly for interactive exploration.

    Args:
        route_to_stops (dict): A dictionary mapping route IDs to lists of stops.

    Returns:
        None
    """
    # Genetating graph instance using Plotly for interactive exploration
    graph = nx.Graph()

    # Add nodes and edges to the graph
    for r_id, stp in route_to_stops.items():
        for i in range(len(stp) - 1):
            graph.add_edge(f"Stop_{stp[i]}", f"Stop_{stp[i+1]}", route=str(r_id))

    pos = nx.spring_layout(graph)

    # building edge trace
    edge_trace = go.Scatter(
        x=[pos[n1][i] for n1, n2 in graph.edges() for i in range(2)], 
        y=[pos[n1][j] for n1, n2 in graph.edges() for j in range(2)],
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',
        text=[f"Route: {graph[n1][n2]['route']}" for n1, n2 in graph.edges()],
        mode='lines'
    )

    # Building node trace
    node_trace = go.Scatter(
        x=[pos[n][0] for n in graph.nodes()], 
        y=[pos[n][1] for n in graph.nodes()],
        mode='markers',
        hoverinfo='text',
        text=list(graph.nodes()), 
        marker=dict(size=10, color='#1f77b4', line_width=2)
    )

    # Building figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title='Delhi Bus Routes Network',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig.show()

# Brute-Force Approach for finding direct routes
def direct_route_brute_force(start_stop, end_stop):
    """
    Find all valid routes between two stops using a brute-force method.

    Args:
        start_stop (int): The ID of the starting stop.
        end_stop (int): The ID of the ending stop.

    Returns:
        list: A list of route IDs (int) that connect the two stops directly.
    """
    routes = []
    for r_id, stp in route_to_stops.items():
        if start_stop in stp and end_stop in stp:
            routes.append(r_id)

    valid_routes = []
    for r_id in routes:
        if start_stop in route_to_stops[r_id] and end_stop in route_to_stops[r_id]:
            valid_routes.append(r_id)

    return valid_routes

# Initialize Datalog predicates for reasoning
pyDatalog.create_terms('RouteHasStop, DirectRoute, OptimalRoute, X, Y, Z, R, R1, R2')  
def initialize_datalog():
    """
    Initialize Datalog terms and predicates for reasoning about routes and stops.

    Returns:
        None
    """
    pyDatalog.clear()  # Clear previous terms
    print("Terms initialized: DirectRoute, RouteHasStop, OptimalRoute")  # Confirmation print

    DirectRoute(R, X, Y) <= RouteHasStop(R, X, Z) & RouteHasStop(R, Y, Y.Z) & (Y.Z == Z + 1)
    OptimalRoute(X, Y, R) <= DirectRoute(R, X, Y)

    create_kb()  # Populate the knowledge base
    add_route_data(route_to_stops)  # Add route data to Datalog
    
# Adding route data to Datalog
def add_route_data(route_to_stops):
    """
    Add the route data to Datalog for reasoning.

    Args:
        route_to_stops (dict): A dictionary mapping route IDs to lists of stops.

    Returns:
        None
    """
    for r_id, stp in route_to_stops.items():
        for st_seq, st_id in enumerate(stp, 1):
            +RouteHasStop(r_id, st_id, st_seq) 

# Function to query direct routes between two stops
def query_direct_routes(start, end):
    """
    Query for direct routes between two stops.

    Args:
        start (int): The ID of the starting stop.
        end (int): The ID of the ending stop.

    Returns:
        list: A sorted list of route IDs (str) connecting the two stops.
    """
    
    qd_routes = []
    for r_id, stps in route_to_stops.items():
        if start in stps and end in stps:
            qd_routes.append(r_id)
    
    return qd_routes

# Forward chaining for optimal route planning
def forward_chaining(start_stop_id, end_stop_id, stop_id_to_include, max_transfers):
    """
    Perform forward chaining to find optimal routes considering transfers.

    Args:
        start_stop_id (int): The starting stop ID.
        end_stop_id (int): The ending stop ID.
        stop_id_to_include (int): The stop ID where a transfer occurs.
        max_transfers (int): The maximum number of transfers allowed.

    Returns:
        list: A list of unique paths (list of tuples) that satisfy the criteria, where each tuple contains:
              - route_id1 (int): The ID of the first route.
              - stop_id (int): The ID of the intermediate stop.
              - route_id2 (int): The ID of the second route.
    """
    r_id_1 = [r_id for r_id, stps in route_to_stops.items() if start_stop_id in stps and stop_id_to_include in stps]
    r_id_2 = [r_id for r_id, stps in route_to_stops.items() if end_stop_id in stps and stop_id_to_include in stps]

    paths = []
    for r1 in r_id_1:
        for r2 in r_id_2:
            if r1 == r2 or max_transfers > 0:
                paths.append((r1, stop_id_to_include, r2))
    return paths

# Backward chaining for optimal route planning
def backward_chaining(start_stop_id, end_stop_id, stop_id_to_include, max_transfers):
    """
    Perform backward chaining to find optimal routes considering transfers.

    Args:
        start_stop_id (int): The starting stop ID.
        end_stop_id (int): The ending stop ID.
        stop_id_to_include (int): The stop ID where a transfer occurs.
        max_transfers (int): The maximum number of transfers allowed.

    Returns:
        list: A list of unique paths (list of tuples) that satisfy the criteria, where each tuple contains:
              - route_id1 (int): The ID of the first route.
              - stop_id (int): The ID of the intermediate stop.
              - route_id2 (int): The ID of the second route.
    """
    r_id_1 = [r_id for r_id, stps in route_to_stops.items() if end_stop_id in stps and stop_id_to_include in stps]
    r_id_2 = [r_id for r_id, stps in route_to_stops.items() if start_stop_id in stps and stop_id_to_include in stps]

    paths = []
    for r1 in r_id_1:
        for r2 in r_id_2:
            if r1 == r2 or max_transfers > 0:
                paths.append((r1, stop_id_to_include, r2))
    return paths

# PDDL-style planning for route finding
def pddl_planning(start_stop_id, end_stop_id, stop_id_to_include, max_transfers):
    """
    Implement PDDL-style planning to find routes with optional transfers.

    Args:
        start_stop_id (int): The starting stop ID.
        end_stop_id (int): The ending stop ID.
        stop_id_to_include (int): The stop ID for a transfer.
        max_transfers (int): The maximum number of transfers allowed.

    Returns:
        list: A list of unique paths (list of tuples) that satisfy the criteria, where each tuple contains:
              - route_id1 (int): The ID of the first route.
              - stop_id (int): The ID of the intermediate stop.
              - route_id2 (int): The ID of the second route.
    """
    stop_to_routes = {}
    for r_id, stps in route_to_stops.items():
        for stop in stps:
            stop_to_routes.setdefault(stop, []).append(r_id)

    r_id_1 = stop_to_routes.get(start_stop_id, [])
    r_id_2 = stop_to_routes.get(end_stop_id, [])
    transfer_routes = stop_to_routes.get(stop_id_to_include, [])

    paths = []
    for r1 in r_id_1:
        if r1 in transfer_routes and r1 in r_id_2:
            paths.append((r1, stop_id_to_include, r1))
        else:
            for r2 in r_id_2:
                if r1 in transfer_routes and r2 in transfer_routes and max_transfers > 0:
                    paths.append((r1, stop_id_to_include, r2))

    return paths

# Function to filter fare data based on an initial fare limit
def prune_data(merged_fare_df, initial_fare):
    """
    Filter fare data based on an initial fare limit.

    Args:
        merged_fare_df (DataFrame): The merged fare DataFrame.
        initial_fare (float): The maximum fare allowed.

    Returns:
        DataFrame: A filtered DataFrame containing only routes within the fare limit.
    """
    return merged_fare_df[merged_fare_df['price'] <= initial_fare]

# Pre-computation of Route Summary
def compute_route_summary(pruned_df):
    """
    Generate a summary of routes based on fare information.

    Args:
        pruned_df (DataFrame): The filtered DataFrame containing fare information.

    Returns:
        dict: A summary of routes with the following structure:
              {
                  route_id (int): {
                      'min_price': float,          # The minimum fare for the route
                      'stops': set                # A set of stop IDs for that route
                  }
              }
    """
    route_summary = {}
    for route_id, data in pruned_df.groupby('route_id'):
        route_summary[route_id] = {
            'min_price': data['price'].min(),
            'stops': set(data['destination_id'])
        }
    return route_summary

# BFS for optimized route planning
def bfs_route_planner_optimized(start_stop_id, end_stop_id, initial_fare, route_summary, max_transfers=3):
    """
    Use Breadth-First Search (BFS) to find the optimal route while considering fare constraints.

    Args:
        start_stop_id (int): The starting stop ID.
        end_stop_id (int): The ending stop ID.
        initial_fare (float): The available fare for the trip.
        route_summary (dict): A summary of routes with fare and stop information.
        max_transfers (int): The maximum number of transfers allowed (default is 3).

    Returns:
        list: A list representing the optimal route with stops and routes taken, structured as:
              [
                  (route_id (int), stop_id (int)),  # Tuple for each stop taken in the route
                  ...
              ]
    """
    if not all([start_stop_id, end_stop_id, route_summary]) or not isinstance(route_summary, dict):
        raise ValueError("Invalid input parameters")
    
    # Early exit if start and end are the same
    if start_stop_id == end_stop_id:
        return [(None, start_stop_id)]
    
    # Priority queue to explore paths with minimal transfers or fares first
    queue = [(0, 0, initial_fare, [(None, start_stop_id)])]  # (transfers, current_cost, remaining_fare, path)
    visited = set([(start_stop_id, 0)])
    opt_path = None

    while queue:
        trans, cur_cost, remaining_fare, cur_path = heapq.heappop(queue)
        cur_stop = cur_path[-1][1]

        if cur_stop == end_stop_id:
            return cur_path[1:]  # Return path, excluding the initial (None, start_stop_id)
        
        if trans < max_transfers:
            for r_id, r_info in route_summary.items():
                if cur_stop in r_info.get('stops', []):
                    for next_stop in r_info['stops']:
                        if next_stop != cur_stop:
                            n_trans = trans + (cur_path[-1][0] != r_id)
                            new_fare = remaining_fare - r_info.get('min_price', 0)

                            if (next_stop, n_trans) not in visited and new_fare >= 0:
                                new_path = cur_path + [(r_id, next_stop)]
                                heapq.heappush(queue, (n_trans, cur_cost + r_info['min_price'], new_fare, new_path))
                                visited.add((next_stop, n_trans))
    
    return opt_path