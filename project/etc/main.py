# Import necessary functions
# from Analysis import univariant_analysis, bivariant_analysis, time_based_analysis, spatial_analysis
from Preprocessing import load_data
from clustering import perform_clustering, plot_clusters
from Visualize_path import calculate_distance_and_motion_vectors, plot_2d_trajectory, plot_3d_trajectory
from Simulations import actual_orbit_simulates

file_path = '../../astrCsv.csv'

# Load data
data = load_data(file_path)

data = calculate_distance_and_motion_vectors(data)
data, clustering_data, kmeans, scaler = perform_clustering(data, 3)
plot_clusters(data, kmeans, scaler)


actual_orbit_simulates(data, 5)
