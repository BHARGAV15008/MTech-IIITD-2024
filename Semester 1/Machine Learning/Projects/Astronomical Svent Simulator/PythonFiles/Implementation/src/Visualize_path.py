import numpy as np
import pandas as pd
from Preprocessing import handle_missing_values
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_distance_and_motion_vectors(data):
    data = handle_missing_values(data)
    data['distance_pc'] = 1 / (data['sy_plx'] / 1000)
    AU_PER_PC = 206265
    motion_RA = data['sy_pmra'] * data['distance_pc'] * AU_PER_PC / 1000
    motion_Dec = data['sy_pmdec'] * data['distance_pc'] * AU_PER_PC / 1000
    motion_Radial = data['st_radv']
    motion_magnitude = np.sqrt(motion_RA**2 + motion_Dec**2 + motion_Radial**2)
    data[['motion_RA', 'motion_Dec', 'motion_Radial', 'motion_magnitude']] = pd.DataFrame({'motion_RA': motion_RA, 'motion_Dec': motion_Dec, 'motion_Radial': motion_Radial, 'motion_magnitude': motion_magnitude})
    return data

def plot_2d_trajectory(data):
    if 'motion_magnitude' not in data.columns:
        print("Error: 'motion_magnitude' column is missing")
        print(f"Columns in data: {data.columns.tolist()}")
        return
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['ra'], data['dec'], data['distance_pc'], c=data['motion_magnitude'], cmap='viridis')
    ax.set_xlabel('RA')
    ax.set_ylabel('Dec')
    ax.set_zlabel('Distance (pc)')
    plt.title('2D Trajectory on Sky Plane')
    plt.show()
    years = 100
    data['future_RA'] = data['ra'] + (data['sy_pmra'] / 1000 * years) / 3600
    data['future_Dec'] = data['dec'] + (data['sy_pmdec'] / 1000 * years) / 3600
    plt.figure(figsize=(10, 8))
    plt.quiver(data['ra'], data['dec'], data['future_RA'] - data['ra'], data['future_Dec'] - data['dec'], angles='xy', scale_units='xy', scale=1, color='blue', alpha=0.6)
    plt.scatter(data['ra'], data['dec'], color='red', s=10, label='Current Position')
    plt.title("Projected Motion Paths of Stars")
    plt.xlabel("RA [deg]")
    plt.ylabel("Dec [deg]")
    plt.legend()
    plt.show()

def plot_3d_trajectory(data):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(data['ra'], data['dec'], data['distance_pc'], data['motion_RA'], data['motion_Dec'], data['motion_Radial'], length=10, normalize=True, color='blue', alpha=0.5)
    ax.scatter(data['ra'], data['dec'], data['distance_pc'], color='red', label='Current Position', s=10)
    ax.set_title("3D Motion Paths of Stars")
    ax.set_xlabel("RA [deg]")
    ax.set_ylabel("Dec [deg]")
    ax.set_zlabel("Distance [pc]")
    plt.legend()
    plt.show()