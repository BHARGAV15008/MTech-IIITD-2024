import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Optional
from utils import compute_orbit_path, compute_orbit_velocity


def actual_orbit_simulates(data: pd.DataFrame, cluster_idx: int) -> Optional[FuncAnimation]:
    """
    Simulate and animate orbital paths for planets in a specific cluster within a galaxy-like space.
    
    Args:
        data: DataFrame containing planetary data with cluster assignments.
        cluster_idx: Index of the cluster to simulate.
        
    Returns:
        Optional[FuncAnimation]: Animation object if successful, None if failed.
    """
    x_list,y_list,z_list=[],[],[]
    pos_df=pd.DataFrame()	
    try:
        # Filter data for the cluster
        #cluster_data = data[data['cluster'] == cluster_idx].copy()	# old
        cluster_data = data
        if len(cluster_data) == 0:
            raise ValueError(f"No planets found in cluster {cluster_idx}.")
        
        # Sample planets if too many
        max_planets = 200  # Reduced for better visualization
        #max_planets = clusture_data.shape[0]  # Reduced for better visualization
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
        print(f"cluster_data.shape:{cluster_data.shape}")
        for idx, planet in cluster_data.iterrows():
            #print(f"planet:\n{planet}")
            if not all(pd.notnull(planet[col]) for col in required_columns):
                print(f"----{planet}[{col}]:{planet[col]}")
                continue
            
            # Pre-compute the full orbital path
            t = np.linspace(0, 2 * np.pi, 500)  # Full orbit in radians
            x_orbit, y_orbit, z_orbit = compute_orbit_path(
                a=planet['pl_orbsmax'],
                e=planet['pl_orbeccen'],
                i=np.radians(planet['pl_orbincl']),
                omega=np.radians(planet['pl_orblper']),
                Omega=np.radians(planet['pl_Omega']),
                t=t
            )


            vx_orbit, vy_orbit, vz_orbit = compute_orbit_velocity(
                a=planet['pl_orbsmax'],
                e=planet['pl_orbeccen'],
                i=np.radians(planet['pl_orbincl']),
                omega=np.radians(planet['pl_orblper']),
                Omega=np.radians(planet['pl_Omega']),
                t=t
            )
            #planet_name="p"+str(idx)
            #pos_df[planet_name+"_x"]=x_orbit;pos_df[planet_name+"_y"]=y_orbit;
            #pos_df[planet_name+"_z"]=z_orbit;
            p_name=planet['pl_name']
            f_name="planet_evolution/"+planet['pl_name']+".csv"
            pd.DataFrame({
                # 'mass':planet['pl_bmasse'],
                'x':x_orbit,
                'y':y_orbit,
                'z':z_orbit,
                'vx':vx_orbit,
                'vy':vy_orbit,
                'vz':vz_orbit
                }).to_csv(f_name,index=False)
            #pd.concat([x_orbit,y_orbit,z_orbit],columns=['x','y','z']).to_csv(f_name)
            #print(f"x_orbit.shape:{x_orbit.shape}")
            #x_list.append(x_orbit);y_list.append(y_orbit);z_list.append(z_orbit);
        '''
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
        '''
    except Exception as e:
        plt.close()
        raise ValueError(f"Simulation failed: {str(e)}")
    #return(x_list,y_list,z_list)
    return(pos_df)


# def compute_orbit_path(a: float, e: float, i: float, omega: float, Omega: float) -> (np.ndarray, np.ndarray, np.ndarray):
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
#     print(f"orbit.shape:{orbit.shape}")
#     #print(f"orbit.size:{orbit.size}")
#     x, y, z = rotation_matrix @ orbit
#     print(f"x.shape:{x.shape}")
    
#     return x, y, z


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
