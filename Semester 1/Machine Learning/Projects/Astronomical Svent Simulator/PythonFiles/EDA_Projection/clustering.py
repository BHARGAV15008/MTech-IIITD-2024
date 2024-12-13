import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def select_random_high_mass_planets(data: pd.DataFrame, n_clusters: int, top_percentile: int = 25) -> np.ndarray:
    """
    Select random planets from the top mass percentile as initial centroids.
    """
    # Calculate mass threshold for top percentile
    mass_threshold = np.percentile(data['pl_bmasse'], 100 - top_percentile)
    # Get high mass planets
    high_mass_planets = data[data['pl_bmasse'] >= mass_threshold]
    # Randomly select n_clusters planets from high mass planets
    selected_indices = np.random.choice(
        high_mass_planets.index, 
        size=min(n_clusters, len(high_mass_planets)), 
        replace=False
    )
    return data.loc[selected_indices, ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']].values

def perform_clustering(data: pd.DataFrame, n_clusters: int = 5, seed: int = 42) -> tuple:
    """
    Perform K-Means clustering using random high-mass planets as initial centroids.
    """
    np.random.seed(seed)
    # Select features for clustering
    features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
    clustering_data = data[features].dropna()
    # Standardize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)
    # Select random high-mass planets as initial centroids
    initial_centroids = select_random_high_mass_planets(clustering_data, n_clusters)
    # Convert initial_centroids to DataFrame before scaling
    initial_centroids_df = pd.DataFrame(initial_centroids, columns=features)
    initial_centroids_scaled = scaler.transform(initial_centroids_df)
    # Perform K-Means clustering
    kmeans = KMeans(
        n_clusters=n_clusters,
        init=initial_centroids_scaled,
        n_init=1,
        random_state=seed
    )
    labels = kmeans.fit_predict(scaled_data)
    # Add cluster labels to data
    clustering_data['cluster'] = labels
    clustering_data['is_centroid'] = clustering_data.index.isin(
        clustering_data.nlargest(n_clusters, 'pl_bmasse').index
    )
    # Add cluster information to original data
    data = data.copy()
    data['cluster'] = pd.NA
    data['is_centroid'] = False
    data.loc[clustering_data.index, 'cluster'] = clustering_data['cluster']
    data.loc[clustering_data.index, 'is_centroid'] = clustering_data['is_centroid']
    return data, clustering_data, kmeans, scaler

def plot_clusters(data: pd.DataFrame, kmeans, scaler, show_stats: bool = True):
    """
    Plot clusters in 3D space and optionally show cluster statistics.
    """
    # Replace NA cluster values with -1 for processing
    data['cluster'] = data['cluster'].fillna(-1)
    features = ['pl_bmasse', 'pl_orbsmax', 'pl_orbeccen']
    # Create 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    # Plot each cluster
    colors = plt.cm.tab10(np.linspace(0, 1, len(data['cluster'].unique())))
    cluster_stats = []
    for cluster, color in zip(sorted(data['cluster'].unique()), colors):
        # Get cluster data
        mask = data['cluster'] == cluster
        cluster_data = data[mask]
        # Plot points
        ax.scatter(
            cluster_data['pl_bmasse'],
            cluster_data['pl_orbsmax'],
            cluster_data['pl_orbeccen'],
            c=[color],
            label=f"Cluster {cluster}" if cluster != -1 else "Unclustered",
            s=30,
            alpha=0.6
        )
        # Calculate cluster statistics if valid cluster
        if cluster != -1:
            stats = {
                'cluster': cluster,
                'size': len(cluster_data),
                'avg_mass': cluster_data['pl_bmasse'].mean(),
                'avg_orbit': cluster_data['pl_orbsmax'].mean(),
                'avg_eccen': cluster_data['pl_orbeccen'].mean()
            }
            cluster_stats.append(stats)
    # Plot centroids
    centroids_unscaled = scaler.inverse_transform(kmeans.cluster_centers_)
    ax.scatter(
        centroids_unscaled[:, 0],
        centroids_unscaled[:, 1],
        centroids_unscaled[:, 2],
        c='red',
        marker='x',
        s=200,
        linewidth=3,
        label='Centroids'
    )
    # Customize plot
    ax.set_xlabel('Planet Mass (Earth masses)')
    ax.set_ylabel('Semi-Major Axis (AU)')
    ax.set_zlabel('Orbital Eccentricity')
    ax.set_title('Exoplanet Clusters based on Physical Properties')
    ax.legend(bbox_to_anchor=(1.15, 1))
    # Adjust view angle
    ax.view_init(elev=20, azim=45)
    # Print cluster statistics if requested
    if show_stats:
        print("\nCluster Statistics:")
        stats_df = pd.DataFrame(cluster_stats)
        stats_df = stats_df.round(2)
        print(stats_df.to_string(index=False))
    plt.tight_layout()
    plt.show()
    return stats_df