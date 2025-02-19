import numpy as np
import pickle
import heapq
from collections import deque
import time

# General Notes:
# - Update the provided file name (code_<RollNumber>.py) as per the instructions.
# - Do not change the function name, number of parameters or the sequence of parameters.
# - The expected output for each function is a path (list of node names)
# - Ensure that the returned path includes both the start node and the goal node, in the correct order.
# - If no valid path exists between the start and goal nodes, the function should return None.


# Algorithm: Iterative Deepening Search (IDS)

# Input:
#   - adj_matrix: Adjacency matrix representing the graph.
#   - start_node: The starting node in the graph.
#   - goal_node: The target node in the graph.

# Return:
#   - A list of node names representing the path from the start_node to the goal_node.
#   - If no path exists, the function should return None.

# Sample Test Cases:

#   Test Case 1:
#     - Start node: 1, Goal node: 2
#     - Return: [1, 7, 6, 2]

#   Test Case 2:
#     - Start node: 5, Goal node: 12
#     - Return: [5, 97, 98, 12]

#   Test Case 3:
#     - Start node: 12, Goal node: 49
#     - Return: None

#   Test Case 4:
#     - Start node: 4, Goal node: 12
#     - Return: [4, 6, 2, 9, 8, 5, 97, 98, 12]

def get_ids_path(adj_matrix, start_node, goal_node):
  start_time = time.time()
  timeout = 15
  def ids(rem_node, live_node, goal_node, visited_node):
    if time.time() - start_time > timeout:
      return None
    
    if rem_node == 0:
      return None
    
    if live_node == goal_node:
      return [live_node]
    
    visited_node.add(live_node)
    
    for nb in range(len(adj_matrix)):
      if adj_matrix[live_node][nb] > 0 and nb not in visited_node:
        if trav_path := ids(rem_node - 1, nb, goal_node, visited_node.copy()) :
          return [live_node] + trav_path
      
    return None
  
  for total_traversal in range(len(adj_matrix)):
    visited_node = set()
    if trav_path:=ids(total_traversal, start_node, goal_node, visited_node) :
      return trav_path
    
  return None

# Algorithm: Bi-Directional Search

# Input:
#   - adj_matrix: Adjacency matrix representing the graph.
#   - start_node: The starting node in the graph.
#   - goal_node: The target node in the graph.

# Return:
#   - A list of node names representing the path from the start_node to the goal_node.
#   - If no path exists, the function should return None.

# Sample Test Cases:

#   Test Case 1:
#     - Start node: 1, Goal node: 2
#     - Return: [1, 7, 6, 2]

#   Test Case 2:
#     - Start node: 5, Goal node: 12
#     - Return: [5, 97, 98, 12]

#   Test Case 3:
#     - Start node: 12, Goal node: 49
#     - Return: None

#   Test Case 4:
#     - Start node: 4, Goal node: 12
#     - Return: [4, 6, 2, 9, 8, 5, 97, 98, 12]

def get_bidirectional_search_path(adj_matrix, start_node, goal_node):
  if start_node == goal_node:
      return [start_node]
  
  # Maintaining queue of traversing node from start and goal nodes
  queue_for_start_node = deque([(start_node, [start_node])])
  queue_for_goal_node = deque([(goal_node, [goal_node])])
  
  visit_node_from_start = {start_node: [start_node]}
  visit_node_from_goal = {goal_node: [goal_node]}
  
  while queue_for_start_node and queue_for_goal_node:
      # Traversing from starting node
      next_node, trav_path = queue_for_start_node.popleft()
      for nearest, path_cost in enumerate(adj_matrix[next_node]):
          if path_cost > 0 and nearest not in visit_node_from_start:
              visit_node_from_start[nearest] = trav_path + [nearest]
              queue_for_start_node.append((nearest, visit_node_from_start[nearest]))
              if nearest in visit_node_from_goal:
                  return visit_node_from_start[nearest] + visit_node_from_goal[nearest][::-1][1:]
      
      # Traversing from goal node
      next_node, trav_path = queue_for_goal_node.popleft()
      for nearest, path_cost in enumerate(adj_matrix[next_node]):
          if path_cost > 0 and nearest not in visit_node_from_goal:
              visit_node_from_goal[nearest] = trav_path + [nearest]
              queue_for_goal_node.append((nearest, visit_node_from_goal[nearest]))
              if nearest in visit_node_from_start:
                  return visit_node_from_goal[nearest] + visit_node_from_start[nearest][::-1][1:]
  
  return None

# Algorithm: A* Search Algorithm

# Input:
#   - adj_matrix: Adjacency matrix representing the graph.
#   - node_attributes: Dictionary of node attributes containing x, y coordinates for heuristic calculations.
#   - start_node: The starting node in the graph.
#   - goal_node: The target node in the graph.

# Return:
#   - A list of node names representing the path from the start_node to the goal_node.
#   - If no path exists, the function should return None.

# Sample Test Cases:

#   Test Case 1:
#     - Start node: 1, Goal node: 2
#     - Return: [1, 7, 6, 2]

#   Test Case 2:
#     - Start node: 5, Goal node: 12
#     - Return: [5, 97, 28, 10, 12]

#   Test Case 3:
#     - Start node: 12, Goal node: 49
#     - Return: None

#   Test Case 4:
#     - Start node: 4, Goal node: 12
#     - Return: [4, 6, 27, 9, 8, 5, 97, 28, 10, 12]

def get_astar_search_path(adj_matrix, node_attributes, start_node, goal_node):
    def euclidean_distance(point1, point2):
        if point1['x'] > point2['x']: x = point1['x'] - point2['x']
        else: x = point2['x'] - point1['x']
        if point1['y'] > point2['y']: y = point1['y'] - point2['y']
        else: y = point2['y'] - point1['y']
        return round((x**2 + y**2) ** 0.5, 5)
    
    def heuristic_cost(node):
        to_node = euclidean_distance(node_attributes[start_node], node_attributes[node])
        to_goal = euclidean_distance(node_attributes[node], node_attributes[goal_node])
        return  round(to_goal + to_node, 5)
    
    h_cost = {}
    for i in range(len(adj_matrix)):
        h_cost[i] = heuristic_cost(i)
    
    live_nodes = [(h_cost[start_node], 0, start_node, [start_node])]
    visited_node = set()
    g_costs = {start_node: 0}
    best_paths = {start_node: [start_node]}

    while live_nodes:
        f_cost, g_cost, current_node, path = heapq.heappop(live_nodes)
        if current_node == goal_node:
            return path
        
        if current_node in visited_node:
            continue
        visited_node.add(current_node)

        for nearest, n_cost in enumerate(adj_matrix[current_node]):
            if n_cost > 0 and nearest not in visited_node:
                u_cost = g_cost + n_cost
                if nearest not in g_costs or u_cost < g_costs[nearest]:
                    g_costs[nearest] = u_cost
                    f_cost = u_cost + h_cost[nearest]
                    best_paths[nearest] = path + [nearest]
                    heapq.heappush(live_nodes, (f_cost, u_cost, nearest, best_paths[nearest]))

    return None


# Algorithm: Bi-Directional Heuristic Search

# Input:
#   - adj_matrix: Adjacency matrix representing the graph.
#   - node_attributes: Dictionary of node attributes containing x, y coordinates for heuristic calculations.
#   - start_node: The starting node in the graph.
#   - goal_node: The target node in the graph.

# Return:
#   - A list of node names representing the path from the start_node to the goal_node.
#   - If no path exists, the function should return None.

# Sample Test Cases:

#   Test Case 1:
#     - Start node: 1, Goal node: 2
#     - Return: [1, 7, 6, 2]

#   Test Case 2:
#     - Start node: 5, Goal node: 12
#     - Return: [5, 97, 98, 12]

#   Test Case 3:
#     - Start node: 12, Goal node: 49
#     - Return: None

#   Test Case 4:
#     - Start node: 4, Goal node: 12
#     - Return: [4, 34, 33, 11, 32, 31, 3, 5, 97, 28, 10, 12]

def get_bidirectional_heuristic_search_path(adj_matrix, node_attributes, start_node, goal_node):
  def euclidean_distance(point1, point2):
        if point1['x'] > point2['x']: x = point1['x'] - point2['x']
        else: x = point2['x'] - point1['x']
        if point1['y'] > point2['y']: y = point1['y'] - point2['y']
        else: y = point2['y'] - point1['y']
        return round((x**2 + y**2) ** 0.5, 5)
    
  def heuristic_cost(node):
      to_node = euclidean_distance(node_attributes[start_node], node_attributes[node])
      to_goal = euclidean_distance(node_attributes[node], node_attributes[goal_node])
      return  round(to_goal + to_node, 5)
    
  h_cost = {}
  for i in range(len(adj_matrix)):
      h_cost[i] = heuristic_cost(i)
    
  # Maintaining queue of traversing node from start and goal nodes
  queue_for_start_node = [(0 + h_cost[start_node], 0, start_node, [start_node])]
  queue_for_goal_node = [(0 + h_cost[goal_node], 0, goal_node, [goal_node])]

  visit_node_from_start = {start_node: (0, [start_node])}
  visit_node_from_goal = {goal_node: (0, [goal_node])}

  while queue_for_start_node and queue_for_goal_node:
      # Traversing from starting node
      f_cost_start, g_cost_start, current_node_start, path_from_start = heapq.heappop(queue_for_start_node)
      for nearest, path_cost in enumerate(adj_matrix[current_node_start]):
          if path_cost > 0:
              g_new = g_cost_start + path_cost
              if nearest not in visit_node_from_start or g_new < visit_node_from_start[nearest][0]:
                  visit_node_from_start[nearest] = (g_new, path_from_start + [nearest])
                  f_new = g_new + h_cost[nearest]
                  heapq.heappush(queue_for_start_node, (f_new, g_new, nearest, path_from_start + [nearest]))

                  if nearest in visit_node_from_goal:
                      return visit_node_from_start[nearest][1] + visit_node_from_goal[nearest][1][::-1][1:]

      # Traversing from goal node
      f_cost_goal, g_cost_goal, current_node_goal, path_from_goal = heapq.heappop(queue_for_goal_node)
      for nearest, path_cost in enumerate(adj_matrix[current_node_goal]):
          if path_cost > 0:
              g_new = g_cost_goal + path_cost
              if nearest not in visit_node_from_goal or g_new < visit_node_from_goal[nearest][0]:
                  visit_node_from_goal[nearest] = (g_new, path_from_goal + [nearest])
                  f_new = g_new + h_cost[nearest]
                  heapq.heappush(queue_for_goal_node, (f_new, g_new, nearest, path_from_goal + [nearest]))

                  if nearest in visit_node_from_start:
                      return visit_node_from_goal[nearest][1] + visit_node_from_start[nearest][1][::-1][1:]

  return None

# Bonus Problem
 
# Input:
# - adj_matrix: A 2D list or numpy array representing the adjacency matrix of the graph.

# Return:
# - A list of tuples where each tuple (u, v) represents an edge between nodes u and v.
#   These are the vulnerable roads whose removal would disconnect parts of the graph.

# Note:
# - The graph is undirected, so if an edge (u, v) is vulnerable, then (v, u) should not be repeated in the output list.
# - If the input graph has no vulnerable roads, return an empty list [].

def bonus_problem(adj_matrix):
    def find_removal(u, parent_node):
        nonlocal vistors_t
        is_node_visited[u] = True
        when_tra[u] = vistors_t
        min_trav[u] = vistors_t
        vistors_t += 1

        for v in range(len(adj_matrix)):
            if adj_matrix[u][v] != 0:
                if not is_node_visited[v]:
                    parent_node[v] = u
                    find_removal(v, parent_node)
                    min_trav[u] = min(min_trav[u], min_trav[v])

                    if min_trav[v] > when_tra[u]:
                        path_removalble.append((u, v))
                elif v != parent_node[u]:
                    min_trav[u] = min(min_trav[u], when_tra[v])

    no_nodes = len(adj_matrix)
    is_node_visited = [False] * no_nodes
    when_tra = [-1] * no_nodes
    min_trav = [-1] * no_nodes
    parent_node = [-1] * no_nodes
    path_removalble = []
    vistors_t = 0

    for i in range(no_nodes):
        if not is_node_visited[i]:
            find_removal(i, parent_node)

    return path_removalble


if __name__ == "__main__":
  adj_matrix = np.load('IIIT_Delhi.npy')
  with open('IIIT_Delhi.pkl', 'rb') as f:
    node_attributes = pickle.load(f)

  start_node = int(input("Enter the start node: "))
  end_node = int(input("Enter the end node: "))

  print(f'Iterative Deepening Search Path: {get_ids_path(adj_matrix,start_node,end_node)}')
  print(f'Bidirectional Search Path: {get_bidirectional_search_path(adj_matrix,start_node,end_node)}')
  print(f'A* Path: {get_astar_search_path(adj_matrix,node_attributes,start_node,end_node)}')
  print(f'Bidirectional Heuristic Search Path: {get_bidirectional_heuristic_search_path(adj_matrix,node_attributes,start_node,end_node)}')
  print(f'Bonus Problem: {bonus_problem(adj_matrix)}')