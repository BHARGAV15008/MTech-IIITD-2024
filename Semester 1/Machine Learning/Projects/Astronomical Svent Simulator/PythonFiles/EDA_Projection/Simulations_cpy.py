import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Optional

from utils import compute_orbit_velocity, compute_orbit_path

'''
def actual_orbit_simulates(data: pd.DataFrame, cluster_idx: int) -> Optional[FuncAnimation]: # type: ignore
    """
    Simulate and animate orbital paths for planets in a specific cluster within a galaxy-like space.
    
    Args:
        data: DataFrame containing planetary data with cluster assignments.
        cluster_idx: Index of the cluster to simulate.
        
    Returns:
        Optional[FuncAnimation]: Animation object if successful, None if failed.
    """
    try:
        # Filter data for the cluster
        cluster_data = data[data['cluster'] == cluster_idx].copy()
        if len(cluster_data) == 0:
            raise ValueError(f"No planets found in cluster {cluster_idx}.")
        
        # Sample planets if too many
        max_planets = 10  # Reduced for better visualization
        if len(cluster_data) > max_planets:
            cluster_data = cluster_data.sample(n=max_planets, random_state=42)
        
        # Set up the figure with a dark background
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d', facecolor='black')
        ax.set_facecolor('black')  # Dark galaxy background
        
        # Plot central star with a glow effect
        ax.scatter([0], [0], [0], color='yellow', s=300, marker='*', 
                   edgecolors='orange', label='Central Star')
        
        # Add random stars in the background
        for _ in range(1000):
            x_star = np.random.uniform(-10, 10)
            y_star = np.random.uniform(-10, 10)
            z_star = np.random.uniform(-10, 10)
            ax.scatter(x_star, y_star, z_star, color='white', s=1, alpha=0.6)
        
        # Initialize storage for orbits and planets
        orbit_lines = []
        planet_points = []
        
        # Required orbital elements
        required_columns = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 
                            'pl_orblper', 'pl_Omega', 'pl_orbper']
        
        # Set up planets
        for idx, planet in cluster_data.iterrows():
            if not all(pd.notnull(planet[col]) for col in required_columns):
                continue
            
            # Pre-compute the full orbital path
            t = np.linspace(0, 2 * np.pi, 500)  # Full orbit in radians
            vx_orbit, vy_orbit, vz_orbit = compute_orbit_velocity(
                a=planet['pl_orbsmax'],
                e=planet['pl_orbeccen'],
                i=np.radians(planet['pl_orbincl']),
                omega=np.radians(planet['pl_orblper']),
                Omega=np.radians(planet['pl_Omega'])
            )
            # yield vx_orbit ,vy_orbit ,vz_orbit
    #         # Plot the orbital path with a glowing effect
    #         orbit_line, = ax.plot(x_orbit, y_orbit, z_orbit, label=f"Orbit {idx}", 
    #                               alpha=0.3, color='cyan', linewidth=0.8)
    #         orbit_lines.append(orbit_line)
            
    #         # Initialize the glowing planet point
    #         planet_point, = ax.plot([x_orbit[0]], [y_orbit[0]], [z_orbit[0]], 'o', 
    #                                 markersize=8, color='lime', alpha=0.8)
    #         planet_points.append((planet_point, x_orbit, y_orbit, z_orbit))
        
    #     # Configure plot
    #     ax.set_xlim(-3, 3)
    #     ax.set_ylim(-3, 3)
    #     ax.set_zlim(-3, 3)
    #     ax.set_xlabel("X [AU]", color='white')
    #     ax.set_ylabel("Y [AU]", color='white')
    #     ax.set_zlabel("Z [AU]", color='white')
    #     ax.tick_params(colors='white')
    #     ax.legend(loc='upper right', fontsize='small', facecolor='black', edgecolor='white')
    #     ax.set_title(f"Galaxy Simulation - Cluster {cluster_idx}", color='white')
        
    #     # Create animation
    #     ani = FuncAnimation(
    #         fig, 
    #         update_orbits,
    #         frames=500,
    #         fargs=(planet_points,),
    #         interval=50,
    #         blit=False  # Set to False for 3D plots
    #     )
        
    #     plt.show()
    #     return ani
    
    except Exception as e:
        plt.close()
        raise ValueError(f"Simulation failed: {str(e)}")
'''
def actual_orbit_simulates(data: pd.DataFrame, cluster_idx: int) -> Optional[FuncAnimation]:
    """
    Simulate and animate orbital paths for planets in a specific cluster within a galaxy-like space.
    
    Args:
        data: DataFrame containing planetary data with cluster assignments.
        cluster_idx: Index of the cluster to simulate.
        
    Returns:
        Optional[FuncAnimation]: Animation object if successful, None if failed.
    """
    try:
        # Filter data for the cluster
        cluster_data = data[data['cluster'] == cluster_idx].copy()
        if len(cluster_data) == 0:
            raise ValueError(f"No planets found in cluster {cluster_idx}.")
        
        # Sample planets if too many
        max_planets = 10  # Reduced for better visualization
        if len(cluster_data) > max_planets:
            cluster_data = cluster_data.sample(n=max_planets, random_state=42)
        
        # Set up the figure with a dark background
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d', facecolor='black')
        ax.set_facecolor('black')  # Dark galaxy background
        
        # Plot central star with a glow effect
        ax.scatter([0], [0], [0], color='yellow', s=300, marker='*', 
                   edgecolors='orange', label='Central Star')
        
        # Add random stars in the background
        for _ in range(1000):
            x_star = np.random.uniform(-10, 10)
            y_star = np.random.uniform(-10, 10)
            z_star = np.random.uniform(-10, 10)
            ax.scatter(x_star, y_star, z_star, color='white', s=1, alpha=0.6)
        
        # Initialize storage for orbits and planets
        orbit_lines = []
        planet_points = []
        
        # Required orbital elements
        required_columns = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 
                            'pl_orblper', 'pl_Omega', 'pl_orbper']
        
        # Set up planets
        for idx, planet in cluster_data.iterrows():
            if not all(pd.notnull(planet[col]) for col in required_columns):
                continue
            
            # Pre-compute the full orbital path
            t = np.linspace(0, 2 * np.pi, 500)  # Full orbit in radians
            x_orbit, y_orbit, z_orbit = compute_orbit_path(
                a=planet['pl_orbsmax'],
                e=planet['pl_orbeccen'],
                i=np.radians(planet['pl_orbincl']),
                omega=np.radians(planet['pl_orblper']),
                Omega=np.radians(planet['pl_Omega'])
            )
            
            # Plot the orbital path with a glowing effect
            orbit_line, = ax.plot(x_orbit, y_orbit, z_orbit, label=f"Orbit {idx}", 
                                  alpha=0.3, color='cyan', linewidth=0.8)
            orbit_lines.append(orbit_line)
            
            # Initialize the glowing planet point
            planet_point, = ax.plot([x_orbit[0]], [y_orbit[0]], [z_orbit[0]], 'o', 
                                    markersize=8, color='lime', alpha=0.8)
            planet_points.append((planet_point, x_orbit, y_orbit, z_orbit))
        
        # Configure plot
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-3, 3)
        ax.set_xlabel("X [AU]", color='white')
        ax.set_ylabel("Y [AU]", color='white')
        ax.set_zlabel("Z [AU]", color='white')
        ax.tick_params(colors='white')
        ax.legend(loc='upper right', fontsize='small', facecolor='black', edgecolor='white')
        ax.set_title(f"Galaxy Simulation - Cluster {cluster_idx}", color='white')
        
        # Create animation
        ani = FuncAnimation(
            fig, 
            update_orbits,
            frames=500,
            fargs=(planet_points,),
            interval=50,
            blit=False  # Set to False for 3D plots
        )
        
        plt.show()
        return ani
    
    except Exception as e:
        plt.close()
        raise ValueError(f"Simulation failed: {str(e)}")


def update_orbits(frame: int, planet_points: List) -> List:
    """
    Update function for animating the planets on their orbits.
    
    Args:
        frame: Current frame number.
        planet_points: List of tuples (planet_point, x_orbit, y_orbit, z_orbit).
    
    Returns:
        List: Updated artist objects.
    """
    for planet_point, x_orbit, y_orbit, z_orbit in planet_points:
        # Update planet position
        idx = frame % len(x_orbit)  # Loop through the orbit
        planet_point.set_data_3d([x_orbit[idx]], [y_orbit[idx]], [z_orbit[idx]])
    
    return [p[0] for p in planet_points]