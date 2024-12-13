# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from typing import List, Optional


# def actual_orbit_simulates(data: pd.DataFrame, cluster_idx: int) -> Optional[FuncAnimation]:
#     """
#     Simulate and animate orbital paths for planets in a specific cluster.
    
#     Args:
#         data: DataFrame containing planetary data with cluster assignments.
#         cluster_idx: Index of the cluster to simulate.
        
#     Returns:
#         Optional[FuncAnimation]: Animation object if successful, None if failed.
#     """
#     try:
#         # Filter data for the cluster
#         cluster_data = data[data['cluster'] == cluster_idx].copy()
#         if len(cluster_data) == 0:
#             raise ValueError(f"No planets found in cluster {cluster_idx}.")
        
#         # Sample planets if too many
#         max_planets = 10  # Reduced for better visualization
#         if len(cluster_data) > max_planets:
#             cluster_data = cluster_data.sample(n=max_planets, random_state=42)
        
#         # Set up the figure
#         fig = plt.figure(figsize=(10, 8))
#         ax = fig.add_subplot(111, projection='3d')
        
#         # Plot central star
#         ax.scatter([0], [0], [0], color='yellow', label='Central Star', 
#                    s=200, marker='*', edgecolors='orange')
        
#         # Initialize storage for orbits and planets
#         orbit_lines = []
#         planet_points = []
        
#         # Required orbital elements
#         required_columns = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 
#                             'pl_orblper', 'pl_Omega', 'pl_orbper']
        
#         # Set up planets
#         for idx, planet in cluster_data.iterrows():
#             if not all(pd.notnull(planet[col]) for col in required_columns):
#                 continue
            
#             # Pre-compute the full orbital path
#             t = np.linspace(0, 2 * np.pi, 500)  # Full orbit in radians
#             x_orbit, y_orbit, z_orbit = compute_orbit_path(
#                 a=planet['pl_orbsmax'],
#                 e=planet['pl_orbeccen'],
#                 i=np.radians(planet['pl_orbincl']),
#                 omega=np.radians(planet['pl_orblper']),
#                 Omega=np.radians(planet['pl_Omega'])
#             )
            
#             # Plot the orbital path
#             orbit_line, = ax.plot(x_orbit, y_orbit, z_orbit, label=f"Orbit {idx}", alpha=0.7)
#             orbit_lines.append(orbit_line)
            
#             # Initialize the planet point
#             planet_point, = ax.plot([x_orbit[0]], [y_orbit[0]], [z_orbit[0]], 'o', markersize=5)
#             planet_points.append((planet_point, x_orbit, y_orbit, z_orbit))
        
#         # Configure plot
#         ax.set_xlim(-3, 3)
#         ax.set_ylim(-3, 3)
#         ax.set_zlim(-3, 3)
#         ax.set_xlabel("X [AU]")
#         ax.set_ylabel("Y [AU]")
#         ax.set_zlabel("Z [AU]")
#         ax.legend(loc='upper right')
#         ax.set_title(f"Orbital Simulation - Cluster {cluster_idx}")
        
#         # Create animation
#         ani = FuncAnimation(
#             fig, 
#             update_orbits,
#             frames=500,
#             fargs=(planet_points,),
#             interval=50,
#             blit=False  # Set to False for 3D plots
#         )
        
#         plt.show()
#         return ani
    
#     except Exception as e:
#         plt.close()
#         raise ValueError(f"Simulation failed: {str(e)}")


# def compute_orbit_path(a: float, e: float, i: float, omega: float, Omega: float) -> (np.ndarray, np.ndarray, np.ndarray): # type: ignore
#     """
#     Compute the full elliptical orbit in 3D space.
    
#     Args:
#         a: Semi-major axis in AU.
#         e: Orbital eccentricity.
#         i: Orbital inclination in radians.
#         omega: Argument of periapsis in radians.
#         Omega: Longitude of ascending node in radians.
    
#     Returns:
#         x, y, z: Arrays representing the orbital path in 3D space.
#     """
#     # True anomaly (v) over one complete orbit
#     v = np.linspace(0, 2 * np.pi, 500)
    
#     # Orbital radius (r) as a function of v
#     r = (a * (1 - e**2)) / (1 + e * np.cos(v))
    
#     # Orbital positions in the orbital plane
#     x_orbit = r * np.cos(v)
#     y_orbit = r * np.sin(v)
#     z_orbit = np.zeros_like(x_orbit)
    
#     # Rotation matrices
#     Rz_Omega = np.array([[np.cos(Omega), -np.sin(Omega), 0],
#                          [np.sin(Omega),  np.cos(Omega), 0],
#                          [0,              0,             1]])
    
#     Rx_i = np.array([[1, 0,            0],
#                      [0, np.cos(i), -np.sin(i)],
#                      [0, np.sin(i),  np.cos(i)]])
    
#     Rz_omega = np.array([[np.cos(omega), -np.sin(omega), 0],
#                          [np.sin(omega),  np.cos(omega), 0],
#                          [0,              0,             1]])
    
#     # Full rotation matrix
#     rotation_matrix = Rz_Omega @ Rx_i @ Rz_omega
    
#     # Rotate the orbit into 3D space
#     orbit = np.array([x_orbit, y_orbit, z_orbit])
#     x, y, z = rotation_matrix @ orbit
    
#     return x, y, z


# def update_orbits(frame: int, planet_points: List) -> List:
#     """
#     Update function for animating the planets on their orbits.
    
#     Args:
#         frame: Current frame number.
#         planet_points: List of tuples (planet_point, x_orbit, y_orbit, z_orbit).
    
#     Returns:
#         List: Updated artist objects.
#     """
#     for planet_point, x_orbit, y_orbit, z_orbit in planet_points:
#         # Update planet position
#         idx = frame % len(x_orbit)  # Loop through the orbit
#         planet_point.set_data_3d([x_orbit[idx]], [y_orbit[idx]], [z_orbit[idx]])
    
#     return [p[0] for p in planet_points]



# # Simulations.py
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from typing import List, Optional
# from utils import get_lcm_of_orbits, simulate_orbit_step


# def actual_orbit_simulates(data: pd.DataFrame, cluster_idx: int) -> Optional[FuncAnimation]:
#     """
#     Simulate and animate orbital paths for planets in a specific cluster.
    
#     Args:
#         data: DataFrame containing planetary data with cluster assignments.
#         cluster_idx: Index of the cluster to simulate.
        
#     Returns:
#         Optional[FuncAnimation]: Animation object if successful, None if failed.
#     """
#     try:
#         # Filter data for the cluster
#         cluster_data = data[data['cluster'] == cluster_idx].copy()
#         if len(cluster_data) == 0:
#             raise ValueError(f"No planets found in cluster {cluster_idx}.")
        
#         # Sample planets if too many
#         max_planets = 60
#         if len(cluster_data) > max_planets:
#             cluster_data = cluster_data.sample(n=max_planets, random_state=42)
        
#         # Set up the figure
#         fig = plt.figure(figsize=(12, 12))
#         ax = fig.add_subplot(111, projection='3d')
        
#         # Plot central star
#         ax.scatter([0], [0], [0], color='yellow', label='Central Star', 
#                    s=200, marker='*', edgecolors='orange')
        
#         # Initialize storage for animation objects
#         planet_lines = []
#         planet_points = []
        
#         # Required orbital elements
#         required_columns = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 
#                             'pl_orblper', 'pl_Omega', 'pl_orbper']
        
#         # Set up planets
#         for idx, planet in cluster_data.iterrows():
#             if not all(pd.notnull(planet[col]) for col in required_columns):
#                 continue
            
#             # Initialize orbital path and position
#             line, = ax.plot([], [], [], label=f"Planet {idx}", alpha=0.5)
#             point, = ax.plot([], [], [], 'o', markersize=5)
#             planet_lines.append(line)
#             planet_points.append(point)
        
#         # Configure plot
#         ax.set_xlim(-3, 3)
#         ax.set_ylim(-3, 3)
#         ax.set_zlim(-3, 3)
#         ax.set_xlabel("X [AU]")
#         ax.set_ylabel("Y [AU]")
#         ax.set_zlabel("Z [AU]")
#         ax.legend(loc='upper right')
#         ax.set_title(f"Orbital Simulation - Cluster {cluster_idx}")
        
#         # Calculate simulation duration
#         orbit_period = get_lcm_of_orbits(cluster_data)
#         frames = min(int(orbit_period), 1000)
        
#         # Create animation
#         ani = FuncAnimation(
#             fig, 
#             update,
#             frames=frames,
#             fargs=(cluster_data, planet_lines, planet_points),
#             interval=50,
#             blit=True
#         )
        
#         plt.show()
#         return ani
    
#     except Exception as e:
#         plt.close()
#         raise ValueError(f"Simulation failed: {str(e)}")


# def update(frame: int, 
#            planetary_data: pd.DataFrame, 
#            planet_lines: List, 
#            planet_points: List) -> List:
#     """
#     Update function for the orbital animation.
    
#     Args:
#         frame: Current frame number.
#         planetary_data: DataFrame containing planetary data.
#         planet_lines: List of line objects for orbital paths.
#         planet_points: List of point objects for planet positions.
        
#     Returns:
#         List: Updated artist objects.
#     """
#     updated_artists = []
    
#     for idx, planet in planetary_data.iterrows():
#         try:
#             # Compute new position
#             x, y, z = simulate_orbit_step(
#                 a=planet['pl_orbsmax'],
#                 e=planet['pl_orbeccen'],
#                 i=planet['pl_orbincl'],
#                 omega=planet['pl_orblper'],
#                 Omega=planet['pl_Omega'],
#                 P=planet['pl_orbper'],
#                 time=frame
#             )
            
#             # Update orbital trail
#             line = planet_lines[planetary_data.index.get_loc(idx)]
#             xdata, ydata, zdata = line.get_data_3d()
#             xdata = np.append(xdata[-100:], x)  # Limit trail length
#             ydata = np.append(ydata[-100:], y)
#             zdata = np.append(zdata[-100:], z)
#             line.set_data_3d(xdata, ydata, zdata)
            
#             # Update planet position
#             point = planet_points[planetary_data.index.get_loc(idx)]
#             point.set_data_3d([x], [y], [z])
            
#             updated_artists.extend([line, point])
        
#         except Exception as e:
#             print(f"Error updating planet {idx}: {str(e)}")
#             continue
    
#     return updated_artists



# # # Simulations.py
# # import numpy as np
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from matplotlib.animation import FuncAnimation
# # from typing import List, Optional
# # from utils import get_lcm_of_orbits, simulate_orbit_step


# # def actual_orbit_simulates(data: pd.DataFrame, cluster_idx: int) -> Optional[FuncAnimation]:
# #     """
# #     Simulate and animate orbital paths for planets in a specific cluster.
    
# #     Args:
# #         data: DataFrame containing planetary data with cluster assignments
# #         cluster_idx: Index of the cluster to simulate
        
# #     Returns:
# #         Optional[FuncAnimation]: Animation object if successful, None if failed
# #     """
# #     try:
# #         # Filter and validate data
# #         cluster_data = data[data['cluster'] == cluster_idx].copy()
# #         if len(cluster_data) == 0:
# #             raise ValueError(f"No planets found in cluster {cluster_idx}")
            
# #         # Sample planets if too many
# #         max_planets = 60
# #         if len(cluster_data) > max_planets:
# #             cluster_data = cluster_data.sample(n=max_planets, random_state=42)
        
# #         # Setup the figure
# #         fig = plt.figure(figsize=(25, 25))
# #         ax = fig.add_subplot(111, projection='3d')
        
# #         # Plot central star
# #         ax.scatter([0], [0], [0], color='yellow', label='Central Star', 
# #                   s=200, marker='*', edgecolors='orange')
        
# #         # Initialize storage for animation objects
# #         planet_lines = []
# #         planet_points = []
        
# #         # Setup planets
# #         required_columns = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 
# #                           'pl_orblper', 'pl_Omega', 'pl_orbper']
        
# #         for idx, planet in cluster_data.iterrows():
# #             # Validate planet data
# #             if not all(pd.notnull(planet[col]) for col in required_columns):
# #                 continue
                
# #             # Create visualization elements for this planet
# #             line, = ax.plot([], [], [], label=f"Planet {idx}", alpha=0.5)
# #             point, = ax.plot([], [], [], 'o', markersize=5)
# #             planet_lines.append(line)
# #             planet_points.append(point)
        
# #         # Configure plot
# #         ax.set_xlim(-2, 2)
# #         ax.set_ylim(-2, 2)
# #         ax.set_zlim(-2, 2)
# #         ax.set_xlabel("X [AU]")
# #         ax.set_ylabel("Y [AU]")
# #         ax.set_zlabel("Z [AU]")
# #         ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
# #         ax.set_title(f"Orbital Simulation - Cluster {cluster_idx}")
        
# #         # Calculate simulation duration
# #         orbit_period = get_lcm_of_orbits(cluster_data)
# #         frames = min(int(orbit_period), 1000)  # Limit maximum frames
        
# #         # Create animation
# #         ani = FuncAnimation(
# #             fig, 
# #             update,
# #             frames=frames,
# #             fargs=(cluster_data, planet_lines, planet_points),
# #             interval=50,
# #             blit=True
# #         )
        
# #         plt.show()
# #         return ani
        
# #     except Exception as e:
# #         plt.close()
# #         raise ValueError(f"Simulation failed: {str(e)}")

# # def update(frame: int, 
# #           planetary_data: pd.DataFrame, 
# #           planet_lines: List, 
# #           planet_points: List) -> List:
# #     """
# #     Update function for the orbital animation.
    
# #     Args:
# #         frame: Current frame number
# #         planetary_data: DataFrame containing planetary data
# #         planet_lines: List of line objects for orbital paths
# #         planet_points: List of point objects for planet positions
        
# #     Returns:
# #         List: Updated artist objects
# #     """
# #     updated_artists = []
    
# #     for idx, planet in planetary_data.iterrows():
# #         try:
# #             # Calculate new position
# #             x, y, z = simulate_orbit_step(
# #                 a=planet['pl_orbsmax'],
# #                 e=planet['pl_orbeccen'],
# #                 i=planet['pl_orbincl'],
# #                 omega=planet['pl_orblper'],
# #                 Omega=planet.get('', 0),
# #                 P=planet['pl_orbper'],
# #                 time=frame
# #             )
            
# #             # Update orbital path
# #             line = planet_lines[planetary_data.index.get_loc(idx)]
# #             xdata, ydata, zdata = line.get_data_3d()
# #             if len(xdata) > 100:  # Limit trail length
# #                 xdata = xdata[-100:]
# #                 ydata = ydata[-100:]
# #                 zdata = zdata[-100:]
# #             xdata = np.append(xdata, x)
# #             ydata = np.append(ydata, y)
# #             zdata = np.append(zdata, z)
# #             line.set_data_3d(xdata, ydata, zdata)
            
# #             # Update planet position
# #             point = planet_points[planetary_data.index.get_loc(idx)]
# #             point.set_data_3d([x], [y], [z])
            
# #             updated_artists.extend([line, point])
            
# #         except Exception as e:
# #             print(f"Error updating planet {idx}: {str(e)}")
# #             continue
    
# #     return updated_artists



# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================


# import pandas as pd
# import numpy as np
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def select_random_high_mass_planets(data: pd.DataFrame, n_clusters: int, top_percentile: int = 25) -> np.ndarray:
#     """
#     Select random planets from the top mass percentile as initial centroids.
    
#     Args:
#         data: DataFrame containing planet data
#         n_clusters: Number of clusters desired
#         top_percentile: Percentile threshold for high-mass planets (e.g., 25 means top 25%)
    
#     Returns:
#         Array of selected planet features to use as initial centroids
#     """
#     # Calculate mass threshold for top percentile
#     mass_threshold = np.percentile(data['pl_bmasse'], 100 - top_percentile)
    
#     # Get high mass planets
#     high_mass_planets = data[data['pl_bmasse'] >= mass_threshold]
    
#     # Randomly select n_clusters planets from high mass planets
#     selected_indices = np.random.choice(
#         high_mass_planets.index, 
#         size=min(n_clusters, len(high_mass_planets)), 
#         replace=False
#     )
    
#     return data.loc[selected_indices, ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']].values

# def perform_clustering(data: pd.DataFrame, n_clusters: int = 5, seed: int = 42) -> tuple:
#     """
#     Perform K-Means clustering using random high-mass planets as initial centroids.
    
#     Args:
#         data: DataFrame containing planet data
#         n_clusters: Number of clusters to form
#         seed: Random seed for reproducibility
    
#     Returns:
#         Tuple of (processed_data, clustering_data, kmeans_model, scaler)
#     """
#     np.random.seed(seed)
    
#     # Select features for clustering
#     features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
#     clustering_data = data[features].dropna()
    
#     # Standardize features
#     scaler = StandardScaler()
#     scaled_data = scaler.fit_transform(clustering_data)
#     scaled_df = pd.DataFrame(scaled_data, columns=features, index=clustering_data.index)
    
#     # Select random high-mass planets as initial centroids
#     initial_centroids = select_random_high_mass_planets(clustering_data, n_clusters)
#     initial_centroids_scaled = scaler.transform(initial_centroids)
    
#     # Perform K-Means clustering
#     kmeans = KMeans(
#         n_clusters=n_clusters,
#         init=initial_centroids_scaled,
#         n_init=1,
#         random_state=seed
#     )
    
#     labels = kmeans.fit_predict(scaled_data)
    
#     # Add cluster labels to data
#     clustering_data['cluster'] = labels
#     clustering_data['is_centroid'] = clustering_data.index.isin(
#         clustering_data.nlargest(n_clusters, 'pl_bmasse').index
#     )
    
#     # Add cluster information to original data
#     data = data.copy()
#     data['cluster'] = pd.NA
#     data['is_centroid'] = False
#     data.loc[clustering_data.index, 'cluster'] = clustering_data['cluster']
#     data.loc[clustering_data.index, 'is_centroid'] = clustering_data['is_centroid']
    
#     return data, clustering_data, kmeans, scaler

# def plot_clusters(data: pd.DataFrame, kmeans, scaler, show_stats: bool = True):
#     """
#     Plot clusters in 3D space and optionally show cluster statistics.
    
#     Args:
#         data: DataFrame containing clustered data
#         kmeans: Fitted KMeans model
#         scaler: Fitted StandardScaler
#         show_stats: Whether to print cluster statistics
#     """
#     features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
    
#     # Create 3D plot
#     fig = plt.figure(figsize=(12, 8))
#     ax = fig.add_subplot(111, projection='3d')
    
#     # Plot each cluster
#     colors = plt.cm.tab10(np.linspace(0, 1, len(data['cluster'].unique())))
    
#     cluster_stats = []
#     for cluster, color in zip(sorted(data['cluster'].unique()), colors):
#         # Get cluster data
#         mask = data['cluster'] == cluster
#         cluster_data = data[mask]
        
#         # Plot points
#         ax.scatter(
#             cluster_data['pl_bmasse'],
#             cluster_data['pl_orbsmax'],
#             cluster_data['pl_orbeccen'],
#             c=[color],
#             label=f"Cluster {cluster}",
#             s=30,
#             alpha=0.6
#         )
        
#         # Calculate cluster statistics
#         stats = {
#             'cluster': cluster,
#             'size': len(cluster_data),
#             'avg_mass': cluster_data['pl_bmasse'].mean(),
#             'avg_orbit': cluster_data['pl_orbsmax'].mean(),
#             'avg_eccen': cluster_data['pl_orbeccen'].mean()
#         }
#         cluster_stats.append(stats)
    
#     # Plot centroids
#     centroids_unscaled = scaler.inverse_transform(kmeans.cluster_centers_)
#     ax.scatter(
#         centroids_unscaled[:, 0],
#         centroids_unscaled[:, 1],
#         centroids_unscaled[:, 2],
#         c='red',
#         marker='x',
#         s=200,
#         linewidth=3,
#         label='Centroids'
#     )
    
#     # Customize plot
#     ax.set_xlabel('Planet Mass (Earth masses)')
#     ax.set_ylabel('Semi-Major Axis (AU)')
#     ax.set_zlabel('Orbital Eccentricity')
#     ax.set_title('Exoplanet Clusters based on Physical Properties')
#     ax.legend(bbox_to_anchor=(1.15, 1))
    
#     # Adjust view angle
#     ax.view_init(elev=20, azim=45)
    
#     # Print cluster statistics if requested
#     if show_stats:
#         print("\nCluster Statistics:")
#         stats_df = pd.DataFrame(cluster_stats)
#         stats_df = stats_df.round(2)
#         print(stats_df.to_string(index=False))
    
#     plt.tight_layout()
#     plt.show()
    
#     return stats_df






# import pandas as pd
# import numpy as np
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def perform_clustering(data: pd.DataFrame, n_clusters: int = 5) -> pd.DataFrame:
#     """
#     Perform K-Means clustering and return the data with cluster labels.
#     """
#     # Select features for clustering
#     features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
#     clustering_data = data[features].dropna()

#     # Standardize features
#     scaler = StandardScaler()
#     scaled_data = scaler.fit_transform(clustering_data)

#     # Find planets with highest mass to initialize centroids
#     high_mass_planets = clustering_data.nlargest(n_clusters, 'pl_bmasse')
#     initial_centroids = high_mass_planets.values

#     # Perform K-Means clustering
#     kmeans = KMeans(n_clusters=n_clusters, init=initial_centroids, n_init=1, random_state=42)
#     labels = kmeans.fit_predict(scaled_data)

#     # Map cluster labels back to original data
#     clustering_data['cluster'] = labels
#     clustering_data['is_centroid'] = clustering_data.index.isin(high_mass_planets.index)

#     # Merge clustering results with original data
#     data = data.merge(clustering_data[['cluster', 'is_centroid']], left_index=True, right_index=True, how='left')

#     return data, clustering_data, kmeans, scaler

# def plot_clusters(data: pd.DataFrame, kmeans, scaler):
#     """
#     Plot clusters in 3D space.
#     """
#     # Extract features and cluster labels
#     features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
    
#     # Create 3D plot
#     fig = plt.figure(figsize=(10, 7))
#     ax = fig.add_subplot(111, projection='3d')

#     # Get unique clusters
#     unique_clusters = data['cluster'].unique()
    
#     # Plot each cluster
#     for cluster in unique_clusters:
#         # Filter data for current cluster
#         mask = data['cluster'] == cluster
#         cluster_points = data[mask][features].values
        
#         # Plot the cluster points
#         ax.scatter(
#             cluster_points[:, 0],  # pl_bmasse
#             cluster_points[:, 1],  # pl_orbsmax
#             cluster_points[:, 2],  # pl_orbeccen
#             label=f"Cluster {cluster}",
#             s=20
#         )

#     # Mark centroids
#     centroids = kmeans.cluster_centers_
#     ax.scatter(
#         centroids[:, 0], centroids[:, 1], centroids[:, 2],
#         c='red', s=100, marker='X', label="Centroids"
#     )

#     # Add labels and legend
#     ax.set_xlabel('Mass (pl_bmasse)')
#     ax.set_ylabel('Semi-Major Axis (pl_orbsmax)')
#     ax.set_zlabel('Eccentricity (pl_orbeccen)')
#     ax.legend()
#     ax.set_title("3D Cluster Visualization")
    
#     # Set view angle for better visualization
#     ax.view_init(elev=30, azim=45)
    
#     plt.show()

# import pandas as pd
# import numpy as np
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


# def perform_clustering(data: pd.DataFrame, n_clusters: int = 5) -> pd.DataFrame:
#     """
#     Perform K-Means clustering and return the data with cluster labels.
#     """
#     # Select features for clustering
#     features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
#     clustering_data = data[features].dropna()

#     # Standardize features
#     scaler = StandardScaler()
#     scaled_data = scaler.fit_transform(clustering_data)

#     # Find planets with highest mass to initialize centroids
#     high_mass_planets = clustering_data.nlargest(n_clusters, 'pl_bmasse')
#     initial_centroids = high_mass_planets.values

#     # Perform K-Means clustering
#     kmeans = KMeans(n_clusters=n_clusters, init=initial_centroids, n_init=1, random_state=42)
#     labels = kmeans.fit_predict(scaled_data)

#     # Map cluster labels back to original data
#     clustering_data['cluster'] = labels
#     clustering_data['is_centroid'] = clustering_data.index.isin(high_mass_planets.index)

#     # Merge clustering results with original data
#     data = data.merge(clustering_data[['cluster', 'is_centroid']], left_index=True, right_index=True, how='left')

#     return data, clustering_data, kmeans, scaler

# def plot_clusters(data: pd.DataFrame, kmeans, scaler):
#     """
#     Plot clusters in 3D space.
#     """
#     # Extract features and cluster labels
#     features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
#     scaled_features = scaler.transform(data[features])
#     labels = data['cluster']

#     # Convert scaled features back to a DataFrame for plotting
#     scaled_data = pd.DataFrame(scaled_features, columns=features)

#     # Create a 3D plot
#     fig = plt.figure(figsize=(10, 7))
#     ax = fig.add_subplot(111, projection='3d')

#     # Plot each cluster
#     for cluster in np.unique(labels):
#         cluster_data = scaled_data[data['cluster'] == cluster]
#         ax.scatter(
#             cluster_data['pl_bmasse'],
#             cluster_data['pl_orbsmax'],
#             cluster_data['pl_orbeccen'],
#             label=f"Cluster {cluster}",
#             s=20
#         )

#     # Mark centroids
#     centroids = kmeans.cluster_centers_
#     ax.scatter(
#         centroids[:, 0], centroids[:, 1], centroids[:, 2],
#         c='red', s=100, marker='X', label="Centroids"
#     )

#     # Add labels and legend
#     ax.set_xlabel('Mass (pl_bmasse)')
#     ax.set_ylabel('Semi-Major Axis (pl_orbsmax)')
#     ax.set_zlabel('Eccentricity (pl_orbeccen)')
#     ax.legend()
#     ax.set_title("3D Cluster Visualization")
#     plt.show()


# # def plot_clusters(data: pd.DataFrame, kmeans, scaler):
# #     """
# #     Plot clusters in 3D space.
# #     """
# #     # Extract features and cluster labels
# #     features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
    
# #     # Ensure no NaNs or infinities in the feature columns
# #     features_data = data[features].dropna()
    
# #     # Scale the feature data
# #     scaled_features = scaler.transform(features_data)
# #     labels = data.loc[features_data.index, 'cluster']  # Match indices after dropping NaNs

# #     # Create a 3D plot
# #     fig = plt.figure(figsize=(10, 7))
# #     ax = fig.add_subplot(111, projection='3d')

# #     # Plot each cluster with different colors
# #     for cluster in np.unique(labels):
# #         cluster_data = scaled_features[labels == cluster]
# #         ax.scatter(
# #             cluster_data[:, 0],  # pl_bmasse
# #             cluster_data[:, 1],  # pl_orbsmax
# #             cluster_data[:, 2],  # pl_orbeccen
# #             label=f"Cluster {cluster}",
# #             s=20
# #         )

# #     # Mark centroids
# #     centroids = kmeans.cluster_centers_
# #     ax.scatter(
# #         centroids[:, 0], centroids[:, 1], centroids[:, 2],
# #         c='red', s=100, marker='X', label="Centroids"
# #     )

# #     # Add labels and legend
# #     ax.set_xlabel('Mass (pl_bmasse)')
# #     ax.set_ylabel('Semi-Major Axis (pl_orbsmax)')
# #     ax.set_zlabel('Eccentricity (pl_orbeccen)')
# #     ax.legend()
# #     ax.set_title("3D Cluster Visualization")
    
# #     # Ensure that the plot does not collapse into a 2D plane
# #     ax.view_init(elev=30, azim=60)  # Set a 3D perspective for better visualization

# #     plt.show()



# # def perform_mass_weighted_clustering(data, n_clusters=3):
# #     """
# #     Perform clustering with KMeans considering planet mass as a weight for the centroids.
# #     """
# #     # Extract relevant features for clustering (e.g., distance, orbital parameters, mass)
# #     X = data[['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_Omega', 'pl_orbper']].copy()
# #     masses = data['pl_mass'].values  # Use mass as the weight for clustering

# #     # Normalize the features (excluding mass)
# #     from sklearn.preprocessing import StandardScaler
# #     scaler = StandardScaler()
# #     X_scaled = scaler.fit_transform(X)

# #     # Perform KMeans clustering
# #     kmeans = KMeans(n_clusters=n_clusters, random_state=42)
# #     kmeans.fit(X_scaled, sample_weight=masses)  # Apply mass as weight

# #     # Assign cluster labels to data
# #     data['cluster'] = kmeans.labels_

# #     return data, kmeans, scaler


# # def calculate_cluster_centroids(data, kmeans):
# #     """
# #     Calculate the mass-weighted centroid for each cluster.
# #     """
# #     centroids = []
# #     for cluster_idx in np.unique(kmeans.labels_):
# #         cluster_data = data[data['cluster'] == cluster_idx]
        
# #         # Get the mass of the planets in this cluster
# #         masses = cluster_data['pl_mass'].values
        
# #         # Calculate the weighted mean of the orbital parameters for the centroid
# #         centroid = np.average(cluster_data[['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_Omega', 'pl_orbper']].values, axis=0, weights=masses)
        
# #         # Store the centroid
# #         centroids.append(centroid)
    
# #     return np.array(centroids)


