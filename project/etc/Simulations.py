# import math 
# from matplotlib.animation import FuncAnimation 
# import numpy as np 
# import matplotlib.pyplot as plt 
# from mpl_toolkits.mplot3d import Axes3D
# import SpaceEnvironment 

# def solve_kepler(M, e, tol=1e-6): 
#     E = M 
#     while True: 
#         delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E)) 
#         E -= delta_E 
#         if abs(delta_E) < tol: 
#             break 
#     return E 

# def simulate_orbit(a, e, i, omega, Omega, P, num_points=500): 
#     mean_anomaly = np.linspace(0, 2 * np.pi, num_points) 
#     i_rad = np.radians(i) 
#     omega_rad = np.radians(omega) 
#     Omega_rad = np.radians(Omega) 
#     E = np.array([solve_kepler(M, e) for M in mean_anomaly]) 
#     true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)) 
#     r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly)) 
#     x_orb = r * np.cos(true_anomaly) 
#     y_orb = r * np.sin(true_anomaly) 
#     z_orb = np.zeros_like(x_orb) 
#     R_i = np.array([[1, 0, 0], 
#                     [0, np.cos(i_rad), -np.sin(i_rad)], 
#                     [0, np.sin(i_rad), np.cos(i_rad)]]) 
#     R_omega = np.array([[np.cos(omega_rad), -np.sin(omega_rad), 0], 
#                         [np.sin(omega_rad), np.cos(omega_rad), 0], 
#                         [0, 0, 1]]) 
#     R_Omega = np.array([[np.cos(Omega_rad), -np.sin(Omega_rad), 0], 
#                         [np.sin(Omega_rad), np.cos(Omega_rad), 0], 
#                         [0, 0, 1]]) 
#     rotation_matrix = R_Omega @ R_i @ R_omega 
#     orbital_coords = np.dot(rotation_matrix, np.vstack((x_orb, y_orb, z_orb))) 
#     return orbital_coords 

# def visualize_orbit(): 
#     a = 1.0  
#     e = 0.2  
#     i = 30   
#     omega = 45  
#     Omega = 60  
#     P = 365.25  
#     orbit_coords = simulate_orbit(a, e, i, omega, Omega, P) 
#     fig = plt.figure(figsize=(10, 8)) 
#     ax = fig.add_subplot(111, projection='3d') 
#     ax.plot(orbit_coords[0], orbit_coords[1], orbit_coords[2], label='Orbital Path', color='blue') 
#     ax.scatter([0], [0], [0], color='orange', label='Star', s=100)  
#     ax.set_title("3D Orbital Path") 
#     ax.set_xlabel("X [AU]") 
#     ax.set_ylabel("Y [AU]") 
#     ax.set_zlabel("Z [AU]") 
#     plt.legend() 
#     plt.show() 

# def simulate_multiple_orbits(data): 
#     plt.figure(figsize=(12, 8)) 
#     ax = plt.axes(projection='3d') 
#     for _, planet in data.iterrows(): 
#         if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']): 
#             a = planet['pl_orbsmax'] 
#             e = planet['pl_orbeccen'] 
#             i = planet.get('pl_orbincl', 0)  
#             omega = planet.get('pl_orblper', 0)  
#             Omega = np.random.uniform(0, 360)  
#             P = planet.get('pl_orbper', 365.25)  
#             coords = simulate_orbit(a, e, i, omega, Omega, P) 
#             ax.plot(coords[0], coords[1], coords[2], alpha=0.6) 
#     ax.set_title("3D Orbits of Multiple Planets") 
#     ax.set_xlabel("X [AU]") 
#     ax.set_ylabel("Y [AU]") 
#     ax.set_zlabel("Z [AU]") 
#     plt.show() 

# frames = 200 

# def simulate_orbit_step(a, e, i, omega, Omega, P, time): 
#     M = 2 * np.pi * (time % P) / P  
#     i_rad = np.radians(i) 
#     omega_rad = np.radians(omega) 
#     Omega_rad = np.radians(Omega) 
#     E = solve_kepler(M, e) 
#     true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)) 
#     r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly)) 
#     x_orb = r * np.cos(true_anomaly) 
#     y_orb = r * np.sin(true_anomaly) 
#     z_orb = 0  
#     R_i = np.array([[1, 0, 0], 
#                     [0, np.cos(i_rad), -np.sin(i_rad)], 
#                     [0, np.sin(i_rad), np.cos(i_rad)]]) 
#     R_omega = np.array([[np.cos(omega_rad), -np.sin(omega_rad), 0], 
#                         [np.sin(omega_rad), np.cos(omega_rad), 0], 
#                         [0, 0, 1]]) 
#     R_Omega = np.array([[np.cos(Omega_rad), -np.sin(Omega_rad), 0], 
#                         [np.sin(Omega_rad), np.cos(Omega_rad), 0], 
#                         [0, 0, 1]]) 
#     rotation_matrix = R_Omega @ R_i @ R_omega 
#     orbital_coords = np.dot(rotation_matrix, np.array([x_orb, y_orb, z_orb])) 
#     return orbital_coords 

# def example_orbit_simulates(): 
#     planetary_data = [ 
#         {'a': 1.0, 'e': 0.2, 'i': 30, 'omega': 45, 'Omega': 60, 'P': 365.25}, 
#         {'a': 1.5, 'e': 0.1, 'i': 10, 'omega': 90, 'Omega': 120, 'P': 687}, 
#         {'a': 0.7, 'e': 0.3, 'i': 45, 'omega': 135, 'Omega': 180, 'P': 224.7} 
#     ] 
#     fig = plt.figure(figsize=(10, 8)) 
#     ax = fig.add_subplot(111, projection='3d') 
#     ax.scatter([0], [0], [0], color='orange', label='Star', s=100) 
#     planet_lines = [] 
#     planet_points = [] 
#     for planet in planetary_data: 
#         line, = ax.plot([], [], [], label=f"Planet {planetary_data.index(planet)+1}") 
#         point, = ax.plot([], [], [], 'o') 
#         planet_lines.append(line) 
#         planet_points.append(point) 
#     ax.set_xlim(-2, 2) 
#     ax.set_ylim(-2, 2) 
#     ax.set_zlim(-2, 2) 
#     ax.set_xlabel("X [AU]") 
#     ax.set_ylabel("Y [AU]") 
#     ax.set_zlabel("Z [AU]") 
#     ax.legend() 
#     ani = FuncAnimation(fig, update, frames=200, fargs=(planetary_data, planet_lines, planet_points), interval=50, blit=False) 
#     plt.show() 

import math


def lcm(a, b): 
    scale_factor = 100  
    a_scaled = int(a * scale_factor) 
    b_scaled = int(b * scale_factor) 
    return abs(a_scaled * b_scaled) // math.gcd(a_scaled, b_scaled) 

def get_lcm_of_orbits(planetary_data): 
    periods = planetary_data['pl_orbper'].tolist() 
    lcm_value = periods[0] 
    for period in periods[1:]: 
        lcm_value = lcm(lcm_value, period) 
    return lcm_value 

# def actual_orbit_simulates(data): 
#     subset_data = data.head(50) 
#     fig = plt.figure(figsize=(25, 25)) 
#     ax = fig.add_subplot(111, projection='3d') 
#     ax.scatter([0], [0], [0], color='orange', label='Star', s=100, marker='*') 
#     planet_lines = [] 
#     planet_points = [] 
#     for idx, planet in subset_data.iterrows(): 
#         if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']): 
#             a = planet['pl_orbsmax'] 
#             e = planet['pl_orbeccen'] 
#             i = planet.get('pl_orbincl', 0) 
#             omega = planet.get('pl_orblper', 0) 
#             Omega = planet.get('pl_Omega', 0) 
#             P = planet.get('pl_orbper', 365.25) 
#             line, = ax.plot([], [], [], label=f"Planet {idx + 1}") 
#             point, = ax.plot([], [], [], 'o') 
#             planet_lines.append(line) 
#             planet_points.append(point) 
#     ax.set_xlim(-2, 2) 
#     ax.set_ylim(-2, 2) 
#     ax.set_zlim(-2, 2) 
#     ax.set_xlabel("X [AU]") 
#     ax.set_ylabel("Y [AU]") 
#     ax.set_zlabel("Z [AU]") 
#     ax.legend() 
#     ani = FuncAnimation(fig, update, frames=get_lcm_of_orbits(data), fargs=(subset_data, planet_lines, planet_points), interval=70, blit=False) 
#     plt.show() 
#     return ani 

# def update(frame, planetary_data, planet_lines, planet_points): 
#     for idx, planet in planetary_data.iterrows(): 
#         a = planet['pl_orbsmax'] 
#         e = planet['pl_orbeccen'] 
#         i = planet.get('pl_orbincl', 0) 
#         omega = planet.get('pl_orblper', 0) 
#         Omega = planet.get('pl_Omega', 0) 
#         P = planet.get('pl_orbper', 365.25) 
#         coords = simulate_orbit_step(a, e, i, omega, Omega, P, time=frame) 
#         xdata, ydata, zdata = planet_lines[idx].get_data_3d() 
#         xdata = np.append(xdata, coords[0]) 
#         ydata = np.append(ydata, coords[1]) 
#         zdata = np.append(zdata, coords[2]) 
#         planet_lines[idx].set_data_3d(xdata, ydata, zdata) 
#         planet_points[idx].set_data_3d([coords[0]], [coords[1]], [coords[2]]) 
#     return planet_lines + planet_points 


# def enhanced_orbit_simulation(data):
#     """Create an enhanced orbital visualization with space environment."""
#     fig = plt.figure(figsize=(20, 20))
#     ax = fig.add_subplot(111, projection='3d')
    
#     # Create space environment
#     space_env = SpaceEnvironment()
#     space_env.add_background_stars(ax)
    
#     # Add some nebulae for visual interest
#     space_env.create_nebula_effect(ax, (5, 5, 0))
#     space_env.create_nebula_effect(ax, (-5, -5, 0))
    
#     # Plot central star
#     ax.scatter([0], [0], [0], color='yellow', s=200, label='Central Star')
    
#     # Plot orbits with enhanced styling
#     subset_data = data.head(20)  # Limit to 20 planets for clarity
#     for idx, planet in subset_data.iterrows():
#         if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']):
#             orbit_coords = simulate_orbit(
#                 planet['pl_orbsmax'],
#                 planet['pl_orbeccen'],
#                 planet.get('pl_orbincl', 0),
#                 planet.get('pl_orblper', 0),
#                 np.random.uniform(0, 360),
#                 planet.get('pl_orbper', 365.25)
#             )
            
#             # Create gradient color for orbit path
#             colors = plt.cm.viridis(np.linspace(0, 1, len(orbit_coords[0])))
            
#             # Plot orbit with varying color and transparency
#             for i in range(len(orbit_coords[0])-1):
#                 ax.plot(orbit_coords[0][i:i+2], 
#                        orbit_coords[1][i:i+2], 
#                        orbit_coords[2][i:i+2],
#                        color=colors[i],
#                        alpha=0.6,
#                        linewidth=1)
    
#     # Styling
#     ax.set_facecolor('black')
#     fig.patch.set_facecolor('black')
#     ax.grid(False)
#     ax.xaxis.label.set_color('white')
#     ax.yaxis.label.set_color('white')
#     ax.zaxis.label.set_color('white')
    
#     # Set labels
#     ax.set_xlabel("X [AU]", fontsize=12)
#     ax.set_ylabel("Y [AU]", fontsize=12)
#     ax.set_zlabel("Z [AU]", fontsize=12)
    
#     plt.title("Enhanced 3D Planetary System Visualization", 
#               color='white', 
#               size=20, 
#               pad=20)
    
#     return fig


# import math
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import pandas as pd
# import matplotlib.animation as animation

# # # Function to solve Kepler's equation
# # def solve_kepler(M, e, tol=1e-6):
# #     E = M
# #     while True:
# #         delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
# #         E -= delta_E
# #         if abs(delta_E) < tol:
# #             break
# #     return E

# # # Simulate orbit around the high mass planet
# # def simulate_orbit(a, e, i, omega, Omega, P, num_points=500):
# #     mean_anomaly = np.linspace(0, 2 * np.pi, num_points)
# #     i_rad = np.radians(i)
# #     omega_rad = np.radians(omega)
# #     Omega_rad = np.radians(Omega)
# #     E = np.array([solve_kepler(M, e) for M in mean_anomaly])
# #     true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
# #     r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly))
# #     x_orb = r * np.cos(true_anomaly)
# #     y_orb = r * np.sin(true_anomaly)
# #     z_orb = np.zeros_like(x_orb)

# #     R_i = np.array([[1, 0, 0],
# #                     [0, np.cos(i_rad), -np.sin(i_rad)],
# #                     [0, np.sin(i_rad), np.cos(i_rad)]])
# #     R_omega = np.array([[np.cos(omega_rad), -np.sin(omega_rad), 0],
# #                         [np.sin(omega_rad), np.cos(omega_rad), 0],
# #                         [0, 0, 1]])
# #     R_Omega = np.array([[np.cos(Omega_rad), -np.sin(Omega_rad), 0],
# #                         [np.sin(Omega_rad), np.cos(Omega_rad), 0],
# #                         [0, 0, 1]])
# #     rotation_matrix = R_Omega @ R_i @ R_omega
# #     orbital_coords = np.dot(rotation_matrix, np.vstack((x_orb, y_orb, z_orb)))
# #     return orbital_coords

# # # Get the high-mass planet from a subset of planets
# # def get_high_mass_planet(data):
# #     # Find the planet with the highest mass (use either pl_bmasse or pl_bmassj depending on availability)
# #     if 'pl_bmassj' in data.columns:
# #         max_mass_planet = data.loc[data['pl_bmassj'].idxmax()]
# #     else:
# #         max_mass_planet = data.loc[data['pl_bmasse'].idxmax()]
# #     return max_mass_planet

# # # Simulate multiple orbits with planets orbiting around the high mass planet
# # def simulate_multiple_orbits_around_high_mass(data):
# #     # Determine the high-mass planet
# #     high_mass_planet = get_high_mass_planet(data)
# #     print(f"High mass planet: {high_mass_planet['pl_bmassj']} Jupiter mass")

# #     # Set up the 3D plot
# #     fig = plt.figure(figsize=(12, 8))
# #     ax = fig.add_subplot(111, projection='3d')

# #     # Plot the high mass planet as the center of attraction
# #     ax.scatter([0], [0], [0], color='orange', label=f'High Mass Planet', s=200)

# #     # Plot orbits for other planets
# #     for _, planet in data.iterrows():
# #         if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']):
# #             a = planet['pl_orbsmax']
# #             e = planet['pl_orbeccen']
# #             i = planet.get('pl_orbincl', 0)
# #             omega = planet.get('pl_orblper', 0)
# #             Omega = np.random.uniform(0, 360)
# #             P = planet.get('pl_orbper', 365.25)

# #             coords = simulate_orbit(a, e, i, omega, Omega, P)
# #             ax.plot(coords[0], coords[1], coords[2], alpha=0.6)

# #     ax.set_title("3D Orbits of Planets Around High Mass Planet")
# #     ax.set_xlabel("X [AU]")
# #     ax.set_ylabel("Y [AU]")
# #     ax.set_zlabel("Z [AU]")
# #     plt.legend()
# #     plt.show()




# # Function to solve Kepler's equation
# def solve_kepler(M, e, tol=1e-6):
#     E = M  # Initial guess for Eccentric Anomaly
#     while True:
#         delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
#         E -= delta_E
#         if abs(delta_E) < tol:
#             break
#     return E

# # Function to simulate orbit around the high mass planet
# def simulate_orbit(a, e, i, omega, Omega, P, num_points=500):
#     # Mean anomaly for each time step
#     mean_anomaly = np.linspace(0, 2 * np.pi, num_points)
    
#     # Inclination and argument of perihelion in radians
#     i_rad = np.radians(i)
#     omega_rad = np.radians(omega)
#     Omega_rad = np.radians(Omega)

#     # Solve Kepler's equation for eccentric anomaly
#     E = np.array([solve_kepler(M, e) for M in mean_anomaly])
    
#     # True anomaly
#     true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    
#     # Orbital radius
#     r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly))

#     # Orbital positions in the orbital plane (2D)
#     x_orb = r * np.cos(true_anomaly)
#     y_orb = r * np.sin(true_anomaly)
#     z_orb = np.zeros_like(x_orb)  # In a 2D orbit for simplicity

#     # Rotation matrices for orbital inclination, argument of perihelion, and longitude of ascending node
#     R_i = np.array([[1, 0, 0],
#                     [0, np.cos(i_rad), -np.sin(i_rad)],
#                     [0, np.sin(i_rad), np.cos(i_rad)]])
#     R_omega = np.array([[np.cos(omega_rad), -np.sin(omega_rad), 0],
#                         [np.sin(omega_rad), np.cos(omega_rad), 0],
#                         [0, 0, 1]])
#     R_Omega = np.array([[np.cos(Omega_rad), -np.sin(Omega_rad), 0],
#                         [np.sin(Omega_rad), np.cos(Omega_rad), 0],
#                         [0, 0, 1]])

#     # Combined rotation matrix
#     rotation_matrix = R_Omega @ R_i @ R_omega

#     # Apply rotation to the orbital coordinates
#     orbital_coords = np.dot(rotation_matrix, np.vstack((x_orb, y_orb, z_orb)))
    
#     return orbital_coords

# # Function to get the high-mass planet
# def get_high_mass_planet(data):
#     if 'pl_bmassj' in data.columns:
#         max_mass_planet = data.loc[data['pl_bmassj'].idxmax()]
#     else:
#         max_mass_planet = data.loc[data['pl_bmasse'].idxmax()]
#     return max_mass_planet

# # Function to animate the orbits
# def animate_orbits(data):
#     # Select a random subset of 20-50 planets
#     subset_data = data.sample(n=np.random.randint(0, 100))
    
#     # Get the high-mass planet
#     high_mass_planet = get_high_mass_planet(subset_data)
#     print(f"High mass planet: {high_mass_planet['pl_bmassj']} Jupiter mass")

#     # Set up the 3D plot
#     fig = plt.figure(figsize=(12, 8))
#     ax = fig.add_subplot(111, projection='3d')
#     ax.set_xlim(-5, 5)
#     ax.set_ylim(-5, 5)
#     ax.set_zlim(-5, 5)
#     ax.set_xlabel("X [AU]")
#     ax.set_ylabel("Y [AU]")
#     ax.set_zlabel("Z [AU]")
#     ax.set_title("3D Orbits of Planets Around High Mass Planet")

#     # Plot the high mass planet at the center
#     ax.scatter([0], [0], [0], color='orange', label=f'High Mass Planet', s=200)

#     # Initialize lines for each planet
#     lines = []
#     for _, planet in subset_data.iterrows():
#         if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']):
#             a = planet['pl_orbsmax']  # Semi-major axis
#             e = planet['pl_orbeccen']  # Eccentricity
#             i = planet.get('pl_orbincl', 0)  # Orbital inclination
#             omega = planet.get('pl_orblper', 0)  # Argument of perihelion
#             Omega = np.random.uniform(0, 360)  # Longitude of ascending node (random)
#             P = planet.get('pl_orbper', 365.25)  # Orbital period (in days)

#             # Simulate orbit
#             coords = simulate_orbit(a, e, i, omega, Omega, P)
#             line, = ax.plot([], [], [], alpha=0.6)
#             lines.append(line)

#     # Function to update the animation
#     def update(frame):
#         for idx, line in enumerate(lines):
#             coords = simulate_orbit(subset_data.iloc[idx]['pl_orbsmax'], 
#                                     subset_data.iloc[idx]['pl_orbeccen'], 
#                                     subset_data.iloc[idx].get('pl_orbincl', 0), 
#                                     subset_data.iloc[idx].get('pl_orblper', 0),
#                                     np.random.uniform(0, 360), 
#                                     subset_data.iloc[idx].get('pl_orbper', 365.25))
#             # Update the orbital path for each planet
#             line.set_data(coords[0][:frame], coords[1][:frame])
#             line.set_3d_properties(coords[2][:frame])
#         return lines

#     # Create the animation
#     ani = animation.FuncAnimation(fig, update, frames=500, interval=50, blit=False)

#     # Show the animation
#     plt.legend()
#     plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from sklearn.cluster import KMeans
# import math

# # Function to simulate orbital motion for planets
# def solve_kepler(M, e, tol=1e-6):
#     E = M
#     while True:
#         delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
#         E -= delta_E
#         if abs(delta_E) < tol:
#             break
#     return E

# def simulate_orbit(a, e, i, omega, Omega, P, num_points=500):
#     mean_anomaly = np.linspace(0, 2 * np.pi, num_points)
#     i_rad = np.radians(i)
#     omega_rad = np.radians(omega)
#     Omega_rad = np.radians(Omega)
#     E = np.array([solve_kepler(M, e) for M in mean_anomaly])
#     true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
#     r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly))
#     x_orb = r * np.cos(true_anomaly)
#     y_orb = r * np.sin(true_anomaly)
#     z_orb = np.zeros_like(x_orb)
#     R_i = np.array([[1, 0, 0],
#                     [0, np.cos(i_rad), -np.sin(i_rad)],
#                     [0, np.sin(i_rad), np.cos(i_rad)]])
#     R_omega = np.array([[np.cos(omega_rad), -np.sin(omega_rad), 0],
#                         [np.sin(omega_rad), np.cos(omega_rad), 0],
#                         [0, 0, 1]])
#     R_Omega = np.array([[np.cos(Omega_rad), -np.sin(Omega_rad), 0],
#                         [np.sin(Omega_rad), np.cos(Omega_rad), 0],
#                         [0, 0, 1]])
#     rotation_matrix = R_Omega @ R_i @ R_omega
#     orbital_coords = np.dot(rotation_matrix, np.vstack((x_orb, y_orb, z_orb)))
#     return orbital_coords

# # Function to simulate multiple orbits with clusters
# def simulate_orbits_with_clusters(data, num_clusters=3):
#     # Extract orbital data (semi-major axis, eccentricity, etc.)
#     orbital_data = data[['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_orbper']].dropna()

#     # Perform KMeans clustering on the orbital data
#     kmeans = KMeans(n_clusters=num_clusters, random_state=42)
#     clusters = kmeans.fit_predict(orbital_data[['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl']])

#     # Get cluster centroids
#     centroids = kmeans.cluster_centers_

#     # Create 3D plot
#     fig = plt.figure(figsize=(12, 10))
#     ax = fig.add_subplot(111, projection='3d')

#     # Plot centroids
#     ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], color='red', s=100, label="Centroids", marker='*')

#     # Plot orbits for each cluster
#     for cluster_idx in range(num_clusters):
#         cluster_data = orbital_data[clusters == cluster_idx]
#         for _, planet in cluster_data.iterrows():
#             a = planet['pl_orbsmax']
#             e = planet['pl_orbeccen']
#             i = planet.get('pl_orbincl', 0)
#             omega = planet.get('pl_orblper', 0)
#             Omega = np.random.uniform(0, 360)  # Randomize Omega for variety
#             P = planet.get('pl_orbper', 365.25)
            
#             orbit_coords = simulate_orbit(a, e, i, omega, Omega, P)
            
#             # Plot each planet's orbit around the centroid
#             ax.plot(orbit_coords[0], orbit_coords[1], orbit_coords[2], alpha=0.6)

#     # Styling
#     ax.set_xlabel("X [AU]")
#     ax.set_ylabel("Y [AU]")
#     ax.set_zlabel("Z [AU]")
#     ax.set_title("Planetary Orbits Around Cluster Centroids")
#     ax.legend()

#     plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# def simulate_orbit_step(a, e, i, omega, Omega, P, time):
#     """
#     Calculate the position of a planet at a given time based on orbital parameters.
#     """
#     omega = np.radians(omega)
#     Omega = np.radians(Omega)
#     i = np.radians(i)
#     M = 2 * np.pi * time / P  # Mean anomaly

#     # Kepler's equation to find eccentric anomaly
#     E = M  # Simplified approximation for small eccentricity
#     nu = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))  # True anomaly
    
#     r = a * (1 - e * np.cos(E))  # Distance from Sun
    
#     # Orbital position in the plane of the orbit
#     x_orbit = r * np.cos(nu)
#     y_orbit = r * np.sin(nu)
#     z_orbit = 0  # Simplified assumption
    
#     # Rotate the position by the inclination, omega, and Omega
#     x = x_orbit * (np.cos(Omega) * np.cos(omega) - np.sin(Omega) * np.sin(omega) * np.cos(i)) - y_orbit * np.cos(Omega) * np.sin(omega)
#     y = x_orbit * (np.sin(Omega) * np.cos(omega) + np.cos(Omega) * np.sin(omega) * np.cos(i)) + y_orbit * np.sin(Omega) * np.sin(omega)
#     z = x_orbit * (np.sin(i) * np.sin(omega)) + y_orbit * np.cos(i)
    
#     return x, y, z

# def actual_orbit_simulates(data, cluster_idx):
#     # Filter data by cluster index
#     cluster_data = data[data['cluster'] == cluster_idx]
    
#     fig = plt.figure(figsize=(25, 25))
#     ax = fig.add_subplot(111, projection='3d')
#     ax.scatter([0], [0], [0], color='orange', label='Star', s=100, marker='*')

#     planet_lines = []
#     planet_points = []
    
#     for idx, planet in cluster_data.iterrows():
#         if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']):
#             a = planet['pl_orbsmax']
#             e = planet['pl_orbeccen']
#             i = planet.get('pl_orbincl', 0)
#             omega = planet.get('pl_orblper', 0)
#             Omega = planet.get('pl_Omega', 0)
#             P = planet.get('pl_orbper', 365.25)
            
#             line, = ax.plot([], [], [], label=f"Planet {idx + 1}")
#             point, = ax.plot([], [], [], 'o')
#             planet_lines.append(line)
#             planet_points.append(point)
    
#     ax.set_xlim(-2, 2)
#     ax.set_ylim(-2, 2)
#     ax.set_zlim(-2, 2)
#     ax.set_xlabel("X [AU]")
#     ax.set_ylabel("Y [AU]")
#     ax.set_zlabel("Z [AU]")
#     ax.legend()
    
#     ani = FuncAnimation(fig, update, frames=get_lcm_of_orbits(data), fargs=(cluster_data, planet_lines, planet_points), interval=70, blit=False)
    
#     plt.show()
#     return ani

# def update(frame, planetary_data, planet_lines, planet_points):
#     """
#     Update function for animation.
#     """
#     for idx, planet in planetary_data.iterrows():
#         a = planet['pl_orbsmax']
#         e = planet['pl_orbeccen']
#         i = planet.get('pl_orbincl', 0)
#         omega = planet.get('pl_orblper', 0)
#         Omega = planet.get('pl_Omega', 0)
#         P = planet.get('pl_orbper', 365.25)
        
#         coords = simulate_orbit_step(a, e, i, omega, Omega, P, time=frame)
        
#         xdata, ydata, zdata = planet_lines[idx].get_data_3d()
#         xdata = np.append(xdata, coords[0])
#         ydata = np.append(ydata, coords[1])
#         zdata = np.append(zdata, coords[2])
        
#         planet_lines[idx].set_data_3d(xdata, ydata, zdata)
#         planet_points[idx].set_data_3d([coords[0]], [coords[1]], [coords[2]])
    
#     return planet_lines + planet_points

# def simulate_orbits_with_clusters(data, kmeans):
#     """
#     Simulate the orbits for each cluster and animate.
#     """
#     num_clusters = len(np.unique(kmeans.labels_))
    
#     for cluster_idx in range(num_clusters):
#         # Call the function to animate the orbits for each cluster
#         actual_orbit_simulates(data, cluster_idx)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate_orbit_step(a, e, i, omega, Omega, P, time):
    """
    Calculate the position of a planet at a given time based on orbital parameters.
    """
    omega = np.radians(omega)
    Omega = np.radians(Omega)
    i = np.radians(i)
    M = 2 * np.pi * time / P  # Mean anomaly

    # Kepler's equation to find eccentric anomaly
    E = M  # Simplified approximation for small eccentricity
    nu = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))  # True anomaly
    
    r = a * (1 - e * np.cos(E))  # Distance from Sun
    
    # Orbital position in the plane of the orbit
    x_orbit = r * np.cos(nu)
    y_orbit = r * np.sin(nu)
    z_orbit = 0  # Simplified assumption
    
    # Rotate the position by the inclination, omega, and Omega
    x = x_orbit * (np.cos(Omega) * np.cos(omega) - np.sin(Omega) * np.sin(omega) * np.cos(i)) - y_orbit * np.cos(Omega) * np.sin(omega)
    y = x_orbit * (np.sin(Omega) * np.cos(omega) + np.cos(Omega) * np.sin(omega) * np.cos(i)) + y_orbit * np.sin(Omega) * np.sin(omega)
    z = x_orbit * (np.sin(i) * np.sin(omega)) + y_orbit * np.cos(i)
    
    return x, y, z

def actual_orbit_simulates(data, cluster_idx):
    # Filter data by cluster index, ensuring 50-60 planets per cluster
    cluster_data = data[data['cluster'] == cluster_idx]
    cluster_data = cluster_data.sample(n=min(60, len(cluster_data)), random_state=42)  # Select 50-60 planets

    fig = plt.figure(figsize=(25, 25))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([0], [0], [0], color='orange', label='Star', s=100, marker='*')

    planet_lines = []
    planet_points = []
    
    for idx, planet in cluster_data.iterrows():
        if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']):
            a = planet['pl_orbsmax']
            e = planet['pl_orbeccen']
            i = planet.get('pl_orbincl', 0)
            omega = planet.get('pl_orblper', 0)
            Omega = planet.get('pl_Omega', 0)
            P = planet.get('pl_orbper', 365.25)
            
            line, = ax.plot([], [], [], label=f"Planet {idx + 1}")
            point, = ax.plot([], [], [], 'o')
            planet_lines.append(line)
            planet_points.append(point)
    
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel("X [AU]")
    ax.set_ylabel("Y [AU]")
    ax.set_zlabel("Z [AU]")
    ax.legend()
    
    ani = FuncAnimation(fig, update, frames=get_lcm_of_orbits(data), fargs=(cluster_data, planet_lines, planet_points), interval=70, blit=False)
    
    plt.show()
    return ani

def update(frame, planetary_data, planet_lines, planet_points):
    """
    Update function for animation.
    """
    for idx, planet in planetary_data.iterrows():
        a = planet['pl_orbsmax']
        e = planet['pl_orbeccen']
        i = planet.get('pl_orbincl', 0)
        omega = planet.get('pl_orblper', 0)
        Omega = planet.get('pl_Omega', 0)
        P = planet.get('pl_orbper', 365.25)
        
        coords = simulate_orbit_step(a, e, i, omega, Omega, P, time=frame)
        
        xdata, ydata, zdata = planet_lines[planetary_data.index.get_loc(idx)].get_data_3d()  # Correct the index access
        xdata = np.append(xdata, coords[0])
        ydata = np.append(ydata, coords[1])
        zdata = np.append(zdata, coords[2])
        
        planet_lines[planetary_data.index.get_loc(idx)].set_data_3d(xdata, ydata, zdata)
        planet_points[planetary_data.index.get_loc(idx)].set_data_3d([coords[0]], [coords[1]], [coords[2]])
    
    return planet_lines + planet_points

# def simulate_orbits_with_clusters(data, kmeans):
#     """
#     Simulate the orbits for each cluster and animate.
#     """
#     num_clusters = len(np.unique(kmeans.labels_))
    
#     for cluster_idx in range(num_clusters):
#         # Call the function to animate the orbits for each cluster
#         actual_orbit_simulates(data, cluster_idx)


# def simulate_orbits_with_star_centroids(data, kmeans, centroids):
#     """
#     Simulate the orbits of planets around their corresponding mass-weighted centroids (stars).
#     """
#     num_clusters = len(np.unique(kmeans.labels_))
    
#     fig = plt.figure(figsize=(25, 25))
#     ax = fig.add_subplot(111, projection='3d')
    
#     # Plot the centroids as stars
#     for idx, centroid in enumerate(centroids):
#         ax.scatter(centroid[0], centroid[1], centroid[2], color='yellow', s=200, label=f'Star {idx + 1}', marker='*')
    
#     planet_lines = []
#     planet_points = []
    
#     # Create the planet paths and points
#     for idx, planet in data.iterrows():
#         cluster_idx = planet['cluster']
#         star_position = centroids[cluster_idx]  # Get the centroid for the planet's cluster
        
#         # Simulate the orbit based on the planet's parameters and the star's position
#         if not np.isnan(planet['pl_orbsmax']) and not np.isnan(planet['pl_orbeccen']):
#             a = planet['pl_orbsmax']
#             e = planet['pl_orbeccen']
#             i = planet.get('pl_orbincl', 0)
#             omega = planet.get('pl_orblper', 0)
#             Omega = planet.get('pl_Omega', 0)
#             P = planet.get('pl_orbper', 365.25)

#             line, = ax.plot([], [], [], label=f"Planet {idx + 1}")
#             point, = ax.plot([], [], [], 'o')
#             planet_lines.append(line)
#             planet_points.append(point)
    
#     ax.set_xlim(-2, 2)
#     ax.set_ylim(-2, 2)
#     ax.set_zlim(-2, 2)
#     ax.set_xlabel("X [AU]")
#     ax.set_ylabel("Y [AU]")
#     ax.set_zlabel("Z [AU]")
#     ax.legend()
    
#     ani = FuncAnimation(fig, update, frames=100, fargs=(data, planet_lines, planet_points, centroids), interval=70, blit=False)
#     plt.show()

#     return ani


# def update(frame, data, planet_lines, planet_points, centroids):
#     """
#     Update function for animation, making planets orbit around their assigned stars.
#     """
#     for idx, planet in data.iterrows():
#         cluster_idx = planet['cluster']
#         star_position = centroids[cluster_idx]  # Get the centroid/star for the planet's cluster
        
#         a = planet['pl_orbsmax']
#         e = planet['pl_orbeccen']
#         i = planet.get('pl_orbincl', 0)
#         omega = planet.get('pl_orblper', 0)
#         Omega = planet.get('pl_Omega', 0)
#         P = planet.get('pl_orbper', 365.25)
        
#         coords = simulate_orbit_step(a, e, i, omega, Omega, P, time=frame)

#         # Adjust the position relative to the star (centroid)
#         xdata, ydata, zdata = planet_lines[data.index.get_loc(idx)].get_data_3d()
#         xdata = np.append(xdata, coords[0] + star_position[0])  # Add the star's position to the planet's orbit
#         ydata = np.append(ydata, coords[1] + star_position[1])
#         zdata = np.append(zdata, coords[2] + star_position[2])

#         planet_lines[data.index.get_loc(idx)].set_data_3d(xdata, ydata, zdata)
#         planet_points[data.index.get_loc(idx)].set_data_3d([coords[0] + star_position[0]], [coords[1] + star_position[1]], [coords[2] + star_position[2]])
    
#     return planet_lines + planet_points


