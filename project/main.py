from Preprocessing import handle_missing_values, load_data, remove_some_columns
from Simulations import actual_orbit_simulates
from clustering import perform_clustering, plot_clusters
file_path = '../../astrCsv.csv'

# Load data
data = load_data(file_path)
data = remove_some_columns(data=data)
data = handle_missing_values(data=data)

data, clustering_data, kmeans, scaler = perform_clustering(data, n_clusters=7)
# print(data.columns.tolist())
# Plot clusters
plot_clusters(data, kmeans, scaler)
# actual_orbit_simulates(data, 6)