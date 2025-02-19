import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import random

class GalaxyVisualizer:
    def __init__(self):
        # Define custom color maps for space objects
        colors = [(0,0,0.4), (0.2,0.2,0.8), (1,1,1)]
        self.space_cmap = LinearSegmentedColormap.from_list('space', colors)
        
    def generate_spiral_arm(self, start_angle, arm_points=1000):
        """Generate points for a spiral arm of the galaxy."""
        t = np.linspace(0, 4*np.pi, arm_points)
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
        theta = np.random.uniform(0, 2*np.pi, bulge_stars)
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
        return fig