# import numpy as np
# import pandas as pd
# from utils import large_omega

# def load_data(file_path: str) -> pd.DataFrame:
#     """Load data from a CSV file."""
#     return pd.read_csv(file_path, low_memory=False, index_col=0)

# def remove_some_columns(data: pd.DataFrame) -> pd.DataFrame:
#     """Remove some columns from the DataFrame."""
#     # substring = 'reflink'
#     for col in data.columns:
#         if 'reflink' in col or 'refname' in col:
#             data.drop(col, axis=1, inplace=True)
    
#     cols = ['hostname',
#             'pl_letter',
#             'hd_name',
#             'hip_name',
#             'tic_id',
#             'gaia_id',
#             'discoverymethod',
#             'disc_locale',
#             'disc_facility',
#             'disc_instrument',
#             'pl_bmassprov',
#             'pl_orbtper_systemref',
#             'pl_tranmid_systemref',
#             'st_metratio',
#             'disc_telescope',
#             'disc_year',
#             'disc_pubdate',
#             'st_spectype']


#     for col in cols:
#         data.drop(col, axis=1, inplace=True)
#     return data

# def convert_rastr_to_degrees(rastr: str) -> float:
#     """Convert Right Ascension in time format to decimal degrees."""
#     if not isinstance(rastr, str):
#         return np.nan

#     time_parts = rastr.split('h')
#     hours = float(time_parts[0])
#     minutes, seconds = time_parts[1].split('m')
#     minutes = float(minutes)
#     seconds = float(seconds.replace('s', ''))

#     return 15 * (hours + minutes / 60 + seconds / 3600)

# def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:
#     """Handle missing values in a DataFrame."""
#     data = large_omega(data)
#     if 'rastr' in data.columns:
#         data['ra_deg'] = data['rastr'].apply(convert_rastr_to_degrees)

#     # Drop columns with > 50% missing values, keeping only the key columns
#     key_columns = [
#         'ra_deg', 'ra', 'dec', 'glon', 'glat', 'sy_pmdec', 
#         'st_radv', 'sy_pmra', 'sy_plx', 'pl_orbper', 'pl_orbincl', 
#         'pl_orblper', 'pl_orbeccen', 'pl_orbsmax'
#     ]
#     missing_threshold = 0.75
#     columns_to_drop = data.columns[data.isnull().mean() > missing_threshold].difference(key_columns)
#     data.drop(columns=columns_to_drop, inplace=True)

#     # Fill numerical columns with median
#     for col in data.select_dtypes(include=[np.number]).columns:
#         data[col] = data[col].fillna(data[col].median())  # Replacing inplace=True with direct assignment

#     # Fill categorical columns with mode, ensure uniform type before filling
#     for col in data.select_dtypes(include=['object']).columns:
#         data[col] = data[col].astype(str)  # Ensure uniform type
#         data[col] = data[col].fillna(data[col].mode()[0])  # Replacing inplace=True with direct assignment

#     # Ensure numerical columns are properly cast
#     data['pl_orbsmax'] = pd.to_numeric(data['pl_orbsmax'], errors='coerce')
#     data['pl_orbeccen'] = pd.to_numeric(data['pl_orbeccen'], errors='coerce')
#     data['pl_orbincl'] = pd.to_numeric(data['pl_orbincl'], errors='coerce')
#     data['pl_orblper'] = pd.to_numeric(data['pl_orblper'], errors='coerce')
#     data['pl_orbper'] = pd.to_numeric(data['pl_orbper'], errors='coerce')

#     return data


# import pandas as pd
# import numpy as np

# def load_data(file_path):
#     """Load the dataset from a given file path."""
#     return pd.read_csv(file_path)

# def remove_nan_and_non_numeric(df):
#     """Remove rows with NaN values and non-numeric entries."""
#     # Drop rows with any NaN values
#     df = df.dropna()

#     # Convert all columns to numeric where possible, dropping rows that cannot be converted
#     for col in df.columns:
#         df[col] = pd.to_numeric(df[col], errors='coerce')
    
#     # Drop rows with NaN values after conversion
#     df = df.dropna()
#     return df

# def preprocess(file_path):
#     """Master function to preprocess the dataset."""
#     df = load_data(file_path)
#     df = remove_nan_and_non_numeric(df)
#     return df

# # Example usage
# file_path = 'csv/data_csv.csv'
# preprocessed_data = preprocess(file_path)
# print(preprocessed_data.head())

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_data(file_path):
    """
    Loads the planet dataset from a CSV file.
    """
    return pd.read_csv(file_path)

'''
def preprocess_data(data):
    """
    Preprocesses the data by scaling the features. 
    """
    # Extract numerical features (excluding 'pl_name')
    features = data[['ra', 'dec', 'pl_orbincl', 'pl_bmasse', 'pl_orbsmax', 'pl_orbeccen', 'pl_orblper', 'pl_orbper', 'x', 'y', 'z']]

    # Standardize the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    return scaled_features

def get_heavy_mass_planet(data):
    """
    Finds the planet with the highest mass in the dataset.
    """
    max_mass_idx = data['pl_bmasse'].idxmax()
    highest_mass_planet = data.iloc[max_mass_idx]
    return highest_mass_planet

def initialize_centroids(data, n_clusters=3):
    """
    Initializes the centroids for clustering. 
    """
    highest_mass_planet = get_heavy_mass_planet(data)
    centroids = np.array([highest_mass_planet[['ra', 'dec', 'pl_orbincl', 'pl_bmasse', 'pl_orbsmax', 
                                                'pl_orbeccen', 'pl_orblper', 'pl_orbper', 'x', 'y', 'z']].values])

    # If more centroids are needed, initialize them randomly from remaining planets
    remaining_planets = data.drop(index=highest_mass_planet.name)
    remaining_planets_features = remaining_planets[['ra', 'dec', 'pl_orbincl', 'pl_bmasse', 'pl_orbsmax', 
                                                    'pl_orbeccen', 'pl_orblper', 'pl_orbper', 'x', 'y', 'z']].values
    kmeans = KMeans(n_clusters=n_clusters - 1, random_state=42)
    kmeans.fit(remaining_planets_features)
    
    return np.vstack([centroids, kmeans.cluster_centers_]), highest_mass_planet
    '''

def preprocess_data(data):
    """
    Preprocesses the data by scaling the features. 
    """
    # Extract numerical features (excluding 'pl_name')
    features = data[['mass', 'x', 'y', 'z', 'vx', 'vy', 'vz']]

    # Standardize the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    return scaled_features


def get_heavy_mass_planet(data):
    """
    Finds the planet with the highest mass in the dataset.
    """
    max_mass_idx = data['mass'].idxmax()
    highest_mass_planet = data.iloc[max_mass_idx]
    return highest_mass_planet

def initialize_centroids(data, n_clusters=3):
    # """
    # Initializes the centroids for clustering. 
    # """
    # highest_mass_planet = get_heavy_mass_planet(data)
    # centroids = np.array([highest_mass_planet[['mass', 'x', 'y', 'z', 'vx', 'vy', 'vz']].values])

    # # If more centroids are needed, initialize them randomly from remaining planets
    # remaining_planets = data.drop(index=highest_mass_planet.name)
    # remaining_planets_features = remaining_planets[['mass', 'x', 'y', 'z', 'vx', 'vy', 'vz']].values
    # print(f"remaining_planets_features.shape:{remaining_planets_features.shape}")
    # kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    # kmeans.fit(remaining_planets_features)
    
    # return np.vstack([centroids, kmeans.cluster_centers_]), highest_mass_planet
    # Extract feature columns (replace with the actual logic to select features)
    feature_columns = data.columns

    # Generate random centroids based on the feature dimensions
    centroids = np.random.rand(n_clusters, len(feature_columns)) * data.max().values
    highest_mass_planet = data.iloc[data['mass'].idxmax()]  # Example to extract relevant info
    print(f"highest_mass_planet:{highest_mass_planet}")
    print(f"centroids:{centroids}")
    print(f"type of highest_mass_planet:{type(highest_mass_planet)}")

    return centroids, highest_mass_planet


'''def perform_clustering(data, centroids, n_clusters=3):
    """
    Perform KMeans clustering with the initialized centroids.
    """
    features = preprocess_data(data)
    
    # Initialize the KMeans model
    kmeans = KMeans(n_clusters=n_clusters, init=centroids, n_init=1, random_state=42)
    
    # Fit the KMeans model

    data['Cluster'] = kmeans.fit_predict(features)
    
    return data, kmeans'''

def perform_clustering(data, initial_centers, n_clusters):
    # Ensure initial_centers match n_clusters
    if initial_centers.shape[0] != n_clusters:
        raise ValueError(f"Number of initial centers ({initial_centers.shape[0]}) "
                         f"does not match the number of clusters ({n_clusters}).")
    
    
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, init=initial_centers, n_init=1)
    data['Cluster'] = kmeans.fit_predict(data)
    
    return data, kmeans

def assign_centroid_info(data, centroids, highest_mass_planet, kmeans):
    """
    Assigns the centroid mass and spatial coordinates to each planet in the dataset.
    """
    # Initialize new columns
    data['centroid_mass'] = np.nan
    data['centroid_x'] = np.nan
    data['centroid_y'] = np.nan
    data['centroid_z'] = np.nan

    # Assign centroid info based on cluster
    for cluster_id in range(len(highest_mass_planet)):
        cluster_planets = data[data['Cluster'] == cluster_id]
        
        centroid_mass = highest_mass_planet['mass']  # Mass is at index 3
        centroid_x, centroid_y, centroid_z = highest_mass_planet['x'], highest_mass_planet['y'], highest_mass_planet['z']  # x, y, z are the last three columns
        
        # Assign the centroid mass and coordinates to all planets in the cluster
        data.loc[cluster_planets.index, 'centroid_mass'] = centroid_mass
        data.loc[cluster_planets.index, 'centroid_x'] = centroid_x
        data.loc[cluster_planets.index, 'centroid_y'] = centroid_y
        data.loc[cluster_planets.index, 'centroid_z'] = centroid_z
    
    return data

def visualize_clusters_3d(data):
    """
    Visualizes the clustered data in a 3D scatter plot (x, y, z).
    """
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Scatter plot with color based on cluster
    sc = ax.scatter(data['x'], data['y'], data['z'], c=data['Cluster'], cmap='viridis', marker='o')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Clustered Planets in 3D Space (X, Y, Z)')
    
    # Add color bar
    plt.colorbar(sc, label='Cluster ID')
    
    plt.show()

def main(file_path, n_clusters=3):
    """
    Main function to execute the clustering workflow.
    """
    # Step 1: Load the data
    data = load_data(file_path)
    
    # Step 2: Initialize the centroids
    centroids, highest_mass_planet = initialize_centroids(data, n_clusters)
    
    # Step 3: Perform clustering
    clustered_data, kmeans_model = perform_clustering(data, centroids, n_clusters)
    
    # Step 4: Assign centroid mass and spatial coordinates
    clustered_data = assign_centroid_info(clustered_data, centroids, highest_mass_planet, kmeans_model)
    
    # Step 5: Visualize the clustering result in 3D
    visualize_clusters_3d(clustered_data)

    clustered_data = clustered_data.drop(['ra', 'dec', 'pl_orbincl', 'pl_orbsmax', 'pl_orbeccen', 'pl_orblper', 'pl_orbper', 'pl_Omega'], axis=1)
    
    return clustered_data, kmeans_model


def main_v2(big_df):
    # load dataframe
    for i, df in enumerate(big_df):
        centroid, highetst_mass_planet = initialize_centroids(df, 1)
        n_clusters = 1
        if 1 != centroid.shape[0]:
            print(f"Adjusting n_clusters to match initial centers: {centroid.shape[0]}")
            n_clusters = centroid.shape[0]
        clustered_data, kmeans_model = perform_clustering(df, centroid, n_clusters=n_clusters)
        clustered_data = assign_centroid_info(clustered_data, centroid, highetst_mass_planet, kmeans_model)
        # visualize_clusters_3d(clustered_data)
        big_df[i] = clustered_data

    return big_df

if __name__ == "__main__":
    # Example usage
    file_path = 'csv/data_csv.csv'  # Provide the path to your CSV file
    n_clusters = 5  # Set the number of clusters you need
    clustered_data, kmeans_model = main(file_path, n_clusters)
    clustered_data.to_csv("csv/final_csv.csv", index=False)
    # print(clustered_data)
