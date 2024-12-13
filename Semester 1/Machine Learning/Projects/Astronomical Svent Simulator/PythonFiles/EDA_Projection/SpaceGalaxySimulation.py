import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
from typing import List, Optional

# Define GalaxyVisualizer class
class GalaxyVisualizer:
    def __init__(self):
        # Define custom color maps for space objects
        colors = [(0, 0, 0.4), (0.2, 0.2, 0.8), (1, 1, 1)]
        self.space_cmap = LinearSegmentedColormap.from_list('space', colors)

    def generate_spiral_arm(self, start_angle, arm_points=1000):
        """Generate points for a spiral arm of the galaxy."""
        t = np.linspace(0, 4 * np.pi, arm_points)
        spiral_constant = 0.2
        r = spiral_constant * t
        x = r * np.cos(t + start_angle)
        y = r * np.sin(t + start_angle)
        z = np.random.normal(0, 0.05, arm_points)
        return x, y, z

    def create_galaxy(self, num_arms=4, stars_per_arm=1000):
        """Create a spiral galaxy visualization."""
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(111, projection='3d')

        # Generate spiral arms
        for i in range(num_arms):
            start_angle = i * (2 * np.pi / num_arms)
            x, y, z = self.generate_spiral_arm(start_angle, stars_per_arm)

            # Add random scatter to make it look more natural
            scatter_amount = 0.1
            x += np.random.normal(0, scatter_amount, stars_per_arm)
            y += np.random.normal(0, scatter_amount, stars_per_arm)

            # Create brightness variation
            brightness = np.random.power(0.5, stars_per_arm)

            # Plot stars with varying sizes and brightness
            sizes = np.random.power(0.5, stars_per_arm) * 20
            ax.scatter(x, y, z, c=brightness, cmap=self.space_cmap, s=sizes, alpha=0.6)

        # Add central bulge
        bulge_stars = 2000
        r = np.random.power(0.5, bulge_stars) * 0.5
        theta = np.random.uniform(0, 2 * np.pi, bulge_stars)
        phi = np.random.uniform(0, np.pi, bulge_stars)

        x_bulge = r * np.sin(phi) * np.cos(theta)
        y_bulge = r * np.sin(phi) * np.sin(theta)
        z_bulge = r * np.cos(phi)

        ax.scatter(x_bulge, y_bulge, z_bulge, c='yellow', s=2, alpha=0.8)

        # Styling
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        plt.title("Spiral Galaxy Visualization", color='white', size=20, pad=20)
        plt.savefig('spiral_galaxy.png')  # Save the figure to a file
        plt.close(fig)  # Close the figure to free up memory
        return fig  # Return only the figure

# Define utility functions
def compute_orbit_path(a: float, e: float, i: float, omega: float, Omega: float) -> (np.ndarray, np.ndarray, np.ndarray):
    """Compute the full elliptical orbit in 3D space."""
    v = np.linspace(0, 2 * np.pi, 500)
    r = (a * (1 - e**2)) / (1 + e * np.cos(v))
    x_orbit = r * np.cos(v)
    y_orbit = r * np.sin(v)
    z_orbit = np.zeros_like(x_orbit)

    # Rotation matrices
    Rz_Omega = np.array([[np.cos(Omega), -np.sin(Omega), 0],
                         [np.sin(Omega),  np.cos(Omega), 0],
                         [0,              0,             1]])

    Rx_i = np.array([[1, 0,            0],
                     [0, np.cos(i), -np.sin(i)],
                     [0, np.sin(i),  np.cos(i)]])

    # Apply rotations
    orbit_path = np.vstack((x_orbit, y_orbit, z_orbit))
    rotated_path = Rz_Omega @ (Rx_i @ orbit_path)

    return rotated_path[0], rotated_path[1], rotated_path[2]

def actual_orbit_simulates(data: pd.DataFrame, cluster_index: int, ax):
    """Simulate and plot the orbit of a planet."""
    # Extract parameters for the specified cluster
    a = data['pl_orbsmax'].iloc[cluster_index]  # Semi-major axis
    e = data['pl_orbeccen'].iloc[cluster_index]  # Eccentricity
    i = data['pl_orbincl'].iloc[cluster_index] * np.pi / 180  # Inclination in radians
    omega = 0  # Argument of periapsis (can be set as needed)
    Omega = 0  # Longitude of ascending node (can be set as needed)

    # Compute orbit path
    x_orbit, y_orbit, z_orbit = compute_orbit_path(a, e, i, omega, Omega)

    # Plot the orbit
    ax.plot(x_orbit, y_orbit, z_orbit, color='orange', linewidth=2)

# Define preprocessing function
def preprocess_data(data: pd.DataFrame):
    """Preprocess the DataFrame to handle missing values and types."""
    columns_to_process = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_orbper']
    
    for col in columns_to_process:
        data.loc[:, col] = data[col].astype(str)  # Ensure uniform type
        data.loc[:, col] = data[col].fillna(data[col].mode()[0])  # Fill NaNs with mode
        data.loc[:, col] = pd.to_numeric(data[col], errors='coerce')  # Convert to numeric

    return data