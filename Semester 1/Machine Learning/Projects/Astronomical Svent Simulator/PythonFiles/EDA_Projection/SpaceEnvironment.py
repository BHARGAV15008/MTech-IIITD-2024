import numpy as np


class SpaceEnvironment:
    def __init__(self):
        self.star_colors = ['white', 'yellow', '#FDB813', '#FF8000', '#FF4000']
        
    def add_background_stars(self, ax, num_stars=1000):
        """Add background stars to the visualization."""
        x = np.random.uniform(-10, 10, num_stars)
        y = np.random.uniform(-10, 10, num_stars)
        z = np.random.uniform(-10, 10, num_stars)
        
        sizes = np.random.power(0.5, num_stars) * 2
        colors = np.random.choice(self.star_colors, num_stars)
        
        ax.scatter(x, y, z, s=sizes, c=colors, alpha=0.6)
        
    def create_nebula_effect(self, ax, center, size=2):
        """Add a nebula-like effect to the visualization."""
        points = 1000
        x = np.random.normal(center[0], size, points)
        y = np.random.normal(center[1], size, points)
        z = np.random.normal(center[2], size, points)
        
        colors = np.random.uniform(0, 1, (points, 4))
        colors[:, 3] = 0.1  # Set alpha
        
        ax.scatter(x, y, z, c=colors, s=50)