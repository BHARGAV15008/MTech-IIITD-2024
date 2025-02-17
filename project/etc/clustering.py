import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def perform_clustering(data: pd.DataFrame, n_clusters: int = 5) -> pd.DataFrame:
    """
    Perform K-Means clustering and return the data with cluster labels.
    """
    # Select features for clustering
    features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
    clustering_data = data[features].dropna()

    # Standardize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)

    # Find planets with highest mass to initialize centroids
    high_mass_planets = clustering_data.nlargest(n_clusters, 'pl_bmasse')
    initial_centroids = high_mass_planets.values

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, init=initial_centroids, n_init=1, random_state=42)
    labels = kmeans.fit_predict(scaled_data)

    # Map cluster labels back to original data
    clustering_data['cluster'] = labels
    clustering_data['is_centroid'] = clustering_data.index.isin(high_mass_planets.index)

    # Merge clustering results with original data
    data = data.merge(clustering_data[['cluster', 'is_centroid']], left_index=True, right_index=True, how='left')

    return data, clustering_data, kmeans, scaler

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


def plot_clusters(data: pd.DataFrame, kmeans, scaler):
    """
    Plot clusters in 3D space.
    """
    # Extract features and cluster labels
    features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
    
    # Ensure no NaNs or infinities in the feature columns
    features_data = data[features].dropna()
    
    # Scale the feature data
    scaled_features = scaler.transform(features_data)
    labels = data.loc[features_data.index, 'cluster']  # Match indices after dropping NaNs

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot each cluster with different colors
    for cluster in np.unique(labels):
        cluster_data = scaled_features[labels == cluster]
        ax.scatter(
            cluster_data[:, 0],  # pl_bmasse
            cluster_data[:, 1],  # pl_orbsmax
            cluster_data[:, 2],  # pl_orbeccen
            label=f"Cluster {cluster}",
            s=20
        )

    # Mark centroids
    centroids = kmeans.cluster_centers_
    ax.scatter(
        centroids[:, 0], centroids[:, 1], centroids[:, 2],
        c='red', s=100, marker='X', label="Centroids"
    )

    # Add labels and legend
    ax.set_xlabel('Mass (pl_bmasse)')
    ax.set_ylabel('Semi-Major Axis (pl_orbsmax)')
    ax.set_zlabel('Eccentricity (pl_orbeccen)')
    ax.legend()
    ax.set_title("3D Cluster Visualization")
    
    # Ensure that the plot does not collapse into a 2D plane
    ax.view_init(elev=30, azim=60)  # Set a 3D perspective for better visualization

    plt.show()



def perform_mass_weighted_clustering(data, n_clusters=3):
    """
    Perform clustering with KMeans considering planet mass as a weight for the centroids.
    """
    # Extract relevant features for clustering (e.g., distance, orbital parameters, mass)
    X = data[['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_Omega', 'pl_orbper']].copy()
    masses = data['pl_mass'].values  # Use mass as the weight for clustering

    # Normalize the features (excluding mass)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X_scaled, sample_weight=masses)  # Apply mass as weight

    # Assign cluster labels to data
    data['cluster'] = kmeans.labels_

    return data, kmeans, scaler


def calculate_cluster_centroids(data, kmeans):
    """
    Calculate the mass-weighted centroid for each cluster.
    """
    centroids = []
    for cluster_idx in np.unique(kmeans.labels_):
        cluster_data = data[data['cluster'] == cluster_idx]
        
        # Get the mass of the planets in this cluster
        masses = cluster_data['pl_mass'].values
        
        # Calculate the weighted mean of the orbital parameters for the centroid
        centroid = np.average(cluster_data[['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_Omega', 'pl_orbper']].values, axis=0, weights=masses)
        
        # Store the centroid
        centroids.append(centroid)
    
    return np.array(centroids)


