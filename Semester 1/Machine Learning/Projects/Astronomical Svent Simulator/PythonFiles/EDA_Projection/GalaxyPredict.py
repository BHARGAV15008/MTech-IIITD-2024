import os
import joblib
from lightgbm import LGBMRegressor
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from utils import calculate_orbital_parameters
import ast
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from Preprocessing import main_v2

'''def version_1():
    galaxies = pd.read_csv('../../initial_fragments.csv')

    # Separating galaxies:
    list_of_dict = []
    list_of_dataframes = []
    for i, galaxy in galaxies.iterrows():
        dict_ = {
            'mass': galaxies.iloc[i, 'mass'],
            'x': galaxies.iloc[i, 'x'],
            'y': galaxies.iloc[i, 'y'],
            'z': galaxies.iloc[i, 'z'],
            'vx': galaxies.iloc[i, 'vx'],
            'vy': galaxies.iloc[i, 'vy'],
            'vz': galaxies.iloc[i, 'vz'],
        }
        list_of_dict.append(dict_)

    # preprocessing list of dict to dataframe
    for i in range(len(list_of_dict)):
        parsed_data = {key: np.array(value.strip('[]').replace('\n', ' ').replace(',', ' ').split(), dtype=float) for key, value in list_of_dict[0].items()}
        df = pd.DataFrame(parsed_data)
        list_of_dataframes.append(df)
    # df = pd.DataFrame(parsed_data)
    X = list_of_dataframes[0].head(10)
    # print(X)
    print(list_of_dataframes[0].head())
    print(list_of_dataframes[1].head())
    print(list_of_dataframes[2].head())
    print(list_of_dataframes[3].head())

    list_of_dataframes = main_v2(list_of_dataframes)

    print(list_of_dataframes[0].head())
    
    
    # print(y_pred_list[0][0][0])
    return list_of_dataframes
'''

import pandas as pd
import numpy as np

def version_1():
    # Load CSV file
    try:
        galaxies = pd.read_csv('../../initial_fragments.csv')
    except FileNotFoundError:
        print("File not found. Please check the path.")
        return

    # Separating galaxies into list of dictionaries
    list_of_dict = []
    for _, galaxy in galaxies.iterrows():
        dict_ = {
            'mass': galaxy['mass'],
            'x': galaxy['x'],
            'y': galaxy['y'],
            'z': galaxy['z'],
            'vx': galaxy['vx'],
            'vy': galaxy['vy'],
            'vz': galaxy['vz'],
        }
        list_of_dict.append(dict_)

    # Converting list of dictionaries to list of dataframes
    list_of_dataframes = []
    for i, galaxy_dict in enumerate(list_of_dict):
        parsed_data = {key: np.array(value.strip('[]').replace('\n', ' ').replace(',', ' ').split(), dtype=float) 
                       if isinstance(value, str) else np.array([value]) for key, value in galaxy_dict.items()}
        df = pd.DataFrame(parsed_data)
        list_of_dataframes.append(df)

    # Print initial dataframes for verification
    for i in range(min(4, len(list_of_dataframes))):  # Avoid index errors
        print(f"Dataframe {i}:\n", list_of_dataframes[i].head())

    # Process the dataframes (ensure main_v2 is defined elsewhere)
    if 'main_v2' in globals():
        list_of_dataframes = main_v2(list_of_dataframes)
    else:
        print("Function 'main_v2' not found. Skipping further processing.")
        return list_of_dataframes

    # Print processed dataframes
    for i in range(min(4, len(list_of_dataframes))):  # Avoid index errors
        print(f"Processed Dataframe {i}:\n", list_of_dataframes[i].head())

    return list_of_dataframes



def version_2():
    dir_path = '../../planet_evolution'
    list_file = os.listdir(dir_path)
    list_file = [os.path.join(dir_path, file) for file in list_file if file.endswith('.csv')]
    df = pd.read_csv(list_file[0])
    # X = df.iloc[:-1]
    # Y = df.iloc[1:]
    # Example: Selecting specific columns for X and y
    X = df.iloc[:-1, :]  # Adjust columns as needed
    Y = df.iloc[1:, :]   # Adjust columns as needed

    print("++-------------------------------------------------------------++")
    print("||-----------------    Dataset:  X and Y    -------------------||")
    print("++-------------------------------------------------------------++")
    print(X.head())
    print()
    print(Y.head())
    print()
    print("++-------------------------------------------------------------++")
    return X, Y


# def version_3():
#     file_path = 'Datasets/updated_training_data.csv'
#     data = pd.read_csv(file_path)
#     X = data[['x', 'y', 'z', 'vx', 'vy', 'vz', 'mass']]
#     # X = data[['x', 'y', 'z', 'vx', 'vy', 'vz', 'mass', 'pl_orbsmax', 'pl_orbper']]
#     Y = data[['pl_orbincl', 'pl_orbsmax', 'pl_orbeccen', 'pl_orblper', 'pl_orbper']]
#     # Y = data[['pl_orbincl', 'pl_orbeccen', 'pl_orblper']]
#     return X, Y


'''def version_4():
    data_path = 'csv/final_csv.csv'
    data = pd.read_csv(data_path)
    data = calculate_orbital_parameters(data=data)
    print(f"Datasets: \n {data.head()}")
    print()
    X = data[['x', 'y', 'z', 'vx', 'vy', 'vz', 'mass', 'centroid_x', 'centroid_y', 'centroid_z', 'centroid_mass']]
    Y = data[['a', 'e', 'i_deg', 'Omega_deg', 'omega_deg', 'nu_deg']]
    print(f"X.shape: {X.shape}, Y.shape: {Y.shape}")
    return X, Y'''


def version_4_2(list_of_dataframe):
    data = list_of_dataframe[0]
    data = calculate_orbital_parameters(data=data)
    # remove nan value and
    # data = data.dropna()
    print(f"Datasets: \n {data.head()}")
    print()
    idx = [i for i, row in data.iterrows() if (row['mass'] <= 0 or row['mass'] == row['centroid_mass'])]
    data.drop(idx, inplace=True)
    X = data[['x', 'y', 'z', 'vx', 'vy', 'vz', 'mass', 'centroid_x', 'centroid_y', 'centroid_z', 'centroid_mass']]
    Y = data[['e','a', 'i_deg', 'Omega_deg', 'omega_deg', 'nu_deg']]
    print(f"X.shape: {X.shape}, Y.shape: {Y.shape}")
    return X, Y

# def feature_engineering(X, y, is_orbital=True):
#     if is_orbital:
#         G = 6.67408e-11 # m^3 kg^-1 s^-2 (Gravitational constant)
#         x2 = X['x'] * X['x']
#         y2 = X['y'] * X['y']
#         z2 = X['z'] * X['z']
#         vx2 = X['vx'] * X['vx']
#         vy2 = X['vy'] * X['vy']
#         vz2 = X['vz'] * X['vz']
#         X['r'] = np.sqrt(x2 + y2 + z2) # Magnitude of position vector (distance from the central body)
#         X['v'] = np.sqrt(vx2 + vy2 + vz2) # Magnitude of velocity vector (speed)
#         X['vr'] = (X['vx'] * X['x'] + X['vy'] * X['y'] + X['vz'] * X['z'])/X['r'] # Radial velocity (speed towards the central body)
#         X['mu'] = G * X['mass'] # Gravitational parameter
#         X['oe'] = (X['v']**2)/2 - X['mu']/X['r'] # Orbital energy

#         # Angular momentum components
#         hx = X['y'] * X['vz'] - X['z'] * X['vy']
#         hy = X['z'] * X['vx'] - X['x'] * X['vz']
#         hz = X['x'] * X['vy'] - X['y'] * X['vx']
#         # X['h'] = np.sqrt(hx**2 + hy**2 + hz**2) # Angular momentum
#         X['hx'] = X['y'] * X['vz'] - X['z'] * X['vy']
#         X['hy'] = X['z'] * X['vx'] - X['x'] * X['vz']
#         X['hz'] = X['x'] * X['vy'] - X['y'] * X['vx']
#         X['h'] = np.sqrt(X['hx']**2 + X['hy']**2 + X['hz']**2) # Angular momentum

#         # Eccentricity vector components
#         X['ex'] = (hy * X['vz'] - hz * X['vy'])/X['mu'] - X['x']/X['r']
#         X['ey'] = (hz * X['vx'] - hx * X['vz'])/X['mu'] - X['y']/X['r']
#         X['ez'] = (hx * X['vy'] - hy * X['vx'])/X['mu'] - X['z']/X['r']

#     else:
#         pass

# def feature_engineering(X, y, is_orbital=True):
#     if is_orbital:
#         G = 6.67408e-11  # Gravitational constant
#         x2, y2, z2 = X['x'] ** 2, X['y'] ** 2, X['z'] ** 2
#         vx2, vy2, vz2 = X['vx'] ** 2, X['vy'] ** 2, X['vz'] ** 2
#         X['r'] = np.sqrt(x2 + y2 + z2)  # Distance from central body
#         X['v'] = np.sqrt(vx2 + vy2 + vz2)  # Speed
#         X['vr'] = (X['vx'] * X['x'] + X['vy'] * X['y'] + X['vz'] * X['z']) / X['r']  # Radial velocity
#         X['mu'] = G * X['mass']  # Gravitational parameter
#         X['oe'] = (X['v']**2) / 2 - X['mu'] / X['r']  # Specific orbital energy

#         # Angular momentum components and magnitude
#         hx = X['y'] * X['vz'] - X['z'] * X['vy']
#         hy = X['z'] * X['vx'] - X['x'] * X['vz']
#         hz = X['x'] * X['vy'] - X['y'] * X['vx']
#         X['h'] = np.sqrt(hx**2 + hy**2 + hz**2)  # Angular momentum magnitude
#         X['hx'], X['hy'], X['hz'] = hx, hy, hz

#         # Eccentricity vector components and magnitude
#         X['ex'] = (hy * X['vz'] - hz * X['vy']) / X['mu'] - X['x'] / X['r']
#         X['ey'] = (hz * X['vx'] - hx * X['vz']) / X['mu'] - X['y'] / X['r']
#         X['ez'] = (hx * X['vy'] - hy * X['vx']) / X['mu'] - X['z'] / X['r']
#         X['e_mag'] = np.sqrt(X['ex']**2 + X['ey']**2 + X['ez']**2)

#         # Additional interaction features
#         X['rv'] = X['r'] * X['v']  # Product of distance and speed
#         X['vr_v_ratio'] = X['vr'] / X['v']  # Radial velocity as a fraction of speed
#         X['energy_h_ratio'] = X['oe'] / X['h']  # Orbital energy to angular momentum ratio

#         # # Orbital period ratio
#         # X['vx_by_vy'] = X['vx'] / X['vy']
#         # X['vy_by_vz'] = X['vy'] / X['vz']
#         # X['vz_by_vx'] = X['vz'] / X['vx']

#         # Central Body Influencer
#         X['cbi'] = X['mass'] / X['r']  # Central body influencer



# def feature_engineering(X, y, is_orbital=True):
#     """
#     Perform feature engineering to calculate orbital parameters for planets 
#     based on their position, velocity, and mass relative to the central body.
    
#     Args:
#         X (pd.DataFrame): DataFrame containing the planet's features.
#         y (pd.DataFrame): DataFrame containing the target values.
#         is_orbital (bool): Flag to indicate if orbital parameters should be calculated.
    
#     Returns:
#         pd.DataFrame: Updated DataFrame with additional orbital parameters.
#     """
#     if is_orbital:
#         G = 6.67430e-11  # Gravitational constant

#         # Calculate relative position and velocity of the planet with respect to the center
#         # Compute relative position
#         X['r'] = np.sqrt((X['x'] - X['centroid_x'])**2 + (X['y'] - X['centroid_y'])**2 + (X['z'] - X['centroid_z'])**2)  # Distance from central body
#         X['v'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)  # Speed of the planet
        
#         # Gravitational parameter of the planet and central body
#         X['mu'] = G * X['mass']  # Gravitational parameter of the planet

#         # Specific orbital energy (OE)
#         X['oe'] = (X['v']**2) / 2 - X['mu'] / X['r']  # Orbital energy

#         # Angular momentum components and magnitude
#         hx = (X['y'] - X['centroid_y']) * X['vz'] - (X['z'] - X['centroid_z']) * X['vy']
#         hy = (X['z'] - X['centroid_z']) * X['vx'] - (X['x'] - X['centroid_x']) * X['vz']
#         hz = (X['x'] - X['centroid_x']) * X['vy'] - (X['y'] - X['centroid_y']) * X['vx']
#         X['h'] = np.sqrt(hx**2 + hy**2 + hz**2)  # Angular momentum magnitude
#         X['hx'], X['hy'], X['hz'] = hx, hy, hz  # Angular momentum components

#         # Eccentricity vector components and magnitude
#         X['ex'] = (hy * X['vz'] - hz * X['vy']) / X['mu'] - (X['x'] - X['centroid_x']) / X['r']
#         X['ey'] = (hz * X['vx'] - hx * X['vz']) / X['mu'] - (X['y'] - X['centroid_y']) / X['r']
#         X['ez'] = (hx * X['vy'] - hy * X['vx']) / X['mu'] - (X['z'] - X['centroid_z']) / X['r']
#         X['e_mag'] = np.sqrt(X['ex']**2 + X['ey']**2 + X['ez']**2)  # Eccentricity magnitude

#         # Inclination (i)
#         X['i'] = np.arccos(X['hz'] / X['h'])
#         X['i_deg'] = np.degrees(X['i'])  # Convert inclination to degrees

#         # Longitude of ascending node (Omega)
#         n = np.cross([0, 0, 1], [X['hx'], X['hy'], X['hz']])
#         n_mag = np.linalg.norm(n)
#         X['Omega'] = np.arccos(n[0] / n_mag) if n_mag != 0 else 0
#         if n[1] < 0:
#             X['Omega'] = 2 * np.pi - X['Omega']
#         X['Omega_deg'] = np.degrees(X['Omega'])  # Convert Omega to degrees

#         # Argument of periapsis (omega)
#         X['omega'] = np.arccos(np.dot(n, [X['ex'], X['ey'], X['ez']]) / (n_mag * X['e_mag']))
#         if X['ez'] < 0:
#             X['omega'] = 2 * np.pi - X['omega']
#         X['omega_deg'] = np.degrees(X['omega'])  # Convert omega to degrees

#         # True anomaly (nu)
#         X['nu'] = np.arccos(np.dot([X['ex'], X['ey'], X['ez']], [X['x'] - X['centroid_x'], X['y'] - X['centroid_y'], X['z'] - X['centroid_z']]) / (X['e_mag'] * X['r']))
#         if np.dot([X['x'] - X['centroid_x'], X['y'] - X['centroid_y'], X['z'] - X['centroid_z']], [X['vx'], X['vy'], X['vz']]) < 0:
#             X['nu'] = 2 * np.pi - X['nu']
#         X['nu_deg'] = np.degrees(X['nu'])  # Convert nu to degrees

#         # Semi-major axis (a)
#         X['a'] = -X['mu'] / (2 * X['oe'])  # Semi-major axis formula from energy

#         # Additional features for interactions (optional)
#         X['rv'] = X['r'] * X['v']  # Product of distance and speed
#         X['vr_v_ratio'] = X['vr'] / X['v']  # Radial velocity as a fraction of speed
#         X['energy_h_ratio'] = X['oe'] / X['h']  # Orbital energy to angular momentum ratio

#         # Central Body Influencer (optional)
#         X['cbi'] = X['mass'] / X['r']  # Central body influencer

#     return X, y

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
'''
def feature_engineering_1(X, y):
    G = 6.6743e-11  # Gravitational constant
    
    # Initialize new feature columns
    X['r'] = np.sqrt((X['x'] - X['centroid_x'])**2 + 
                     (X['y'] - X['centroid_y'])**2 + 
                     (X['z'] - X['centroid_z'])**2)
    
    X['v'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)
    
    X['relative_mass'] = X['mass'] / X['centroid_mass']
    
    X['potential_energy'] = -G * X['mass'] * X['centroid_mass'] / X['r']
    X['kinetic_energy'] = 0.5 * X['mass'] * X['v']**2
    
    X['binding_energy'] = X['kinetic_energy'] + X['potential_energy']
    
    # Semi-major axis (a)
    mu = G * (X['mass'] + X['centroid_mass'])
    X['specific_orbital_energy'] = (X['v']**2) / 2 - mu / X['r']
    X['semi_major_axis'] = -mu / (2 * X['specific_orbital_energy'])
    
    # Angular Momentum
    X['hx'] = (X['y'] - X['centroid_y']) * X['vz'] - (X['z'] - X['centroid_z']) * X['vy']
    X['hy'] = (X['z'] - X['centroid_z']) * X['vx'] - (X['x'] - X['centroid_x']) * X['vz']
    X['hz'] = (X['x'] - X['centroid_x']) * X['vy'] - (X['y'] - X['centroid_y']) * X['vx']
    X['angular_momentum'] = np.sqrt(X['hx']**2 + X['hy']**2 + X['hz']**2)
    
    # Eccentricity
    position_vec = X[['x', 'y', 'z']].values - X[['centroid_x', 'centroid_y', 'centroid_z']].values
    velocity_vec = X[['vx', 'vy', 'vz']].values
    h_vec = X[['hx', 'hy', 'hz']].values
    
    e_vec = (np.cross(velocity_vec, h_vec) / mu[:, None]) - (position_vec / X['r'].values[:, None])
    X['eccentricity'] = np.linalg.norm(e_vec, axis=1)
    X['eccentricity'] = np.abs(X['eccentricity'])  # Ensure non-negative eccentricity
    
    # Periapsis and Apoapsis
    X['periapsis'] = X['semi_major_axis'] * (1 - X['eccentricity'])
    X['apoapsis'] = X['semi_major_axis'] * (1 + X['eccentricity'])
    
    # Angular Features
    X['inclination'] = np.arccos(X['hz'] / X['angular_momentum']) * (180 / np.pi)
    
    # Normalize selected features
    scaler = MinMaxScaler()
    X[['semi_major_axis', 'binding_energy', 'r', 'v']] = scaler.fit_transform(X[['semi_major_axis', 'binding_energy', 'r', 'v']])
    
    G = 6.6743e-11  # Gravitational constant
    
    # Orbital period
    X['orbital_period'] = 2 * np.pi * np.sqrt((X['semi_major_axis']**3) / (G * (X['mass'] + X['centroid_mass'])))
    
    # Mean motion
    X['mean_motion'] = np.sqrt(G * (X['mass'] + X['centroid_mass']) / X['semi_major_axis']**3)
    
    # Energy ratios
    X['energy_ratio'] = X['kinetic_energy'] / np.abs(X['potential_energy'])
    
    # Log transformations
    X['log_binding_energy'] = np.log1p(-X['binding_energy'])
    X['log_semi_major_axis'] = np.log1p(X['semi_major_axis'])
    return X, y
'''



import numpy as np
import pandas as pd

def feature_engineering(X, y, is_orbital=True):
    """
    Perform feature engineering to calculate orbital parameters for planets 
    based on their position, velocity, and mass relative to the central body.
    
    Args:
        X (pd.DataFrame): DataFrame containing the planet's features.
        y (pd.DataFrame): DataFrame containing the target values.
        is_orbital (bool): Flag to indicate if orbital parameters should be calculated.
    
    Returns:
        pd.DataFrame: Updated DataFrame with additional orbital parameters.
    """
    if is_orbital:
        G = 6.67430e-11  # Gravitational constant

        # Calculate relative position and velocity of the planet with respect to the center
        # COmputer relative position to x, y , z
        X['rx'] = X['x'] - X['centroid_x']
        X['ry'] = X['y'] - X['centroid_y']
        X['rz'] = X['z'] - X['centroid_z']

        # Compute relative position
        X['r'] = np.sqrt((X['x'] - X['centroid_x'])**2 + 
                         (X['y'] - X['centroid_y'])**2 + 
                         (X['z'] - X['centroid_z'])**2)  # Distance from central body
        X['v'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)  # Speed of the planet

        # Avoid division by zero in 'r'
        # X['r'] = X['r'].replace(0, np.nan)  # Replace zero with NaN to avoid division errors
        
        # Gravitational parameter of the planet and central body
        X['mu'] = G * (X['mass'] + X['centroid_mass'])  # Gravitational parameter of the planet

        # Specific orbital energy (OE)
        X['oe'] = (X['v']**2) / 2 - X['mu'] / X['r']  # Orbital energy

        # Angular momentum components and magnitude
        X['hx'] = (X['y'] - X['centroid_y']) * X['vz'] - (X['z'] - X['centroid_z']) * X['vy']
        X['hy'] = (X['z'] - X['centroid_z']) * X['vx'] - (X['x'] - X['centroid_x']) * X['vz']
        X['hz'] = (X['x'] - X['centroid_x']) * X['vy'] - (X['y'] - X['centroid_y']) * X['vx']
        h = np.array([X['hx'], X['hy'], X['hz']]).T  # Ensure it's a 2D array, each row is a 3D vector
        X['h'] = np.linalg.norm(h, axis=1)  # Magnitude of angular momentum

        # Avoid division by zero in 'h'
        # X['h'] = X['h'].replace(0, np.nan)

        # Eccentricity vector components and magnitude
        X['ex'] = (X['hy'] * X['vz'] - X['hz'] * X['vy']) / X['mu'] - (X['x'] - X['centroid_x']) / X['r']
        X['ey'] = (X['hz'] * X['vx'] - X['hx'] * X['vz']) / X['mu'] - (X['y'] - X['centroid_y']) / X['r']
        X['ez'] = (X['hx'] * X['vy'] - X['hy'] * X['vx']) / X['mu'] - (X['z'] - X['centroid_z']) / X['r']
        X['e_mag'] = np.sqrt(X['ex']**2 + X['ey']**2 + X['ez']**2)  # Eccentricity magnitude

        # Avoid division by zero in 'e_mag'
        # X['e_mag'] = X['e_mag'].replace(0, np.nan)

        # Inclination (i)
        X['i'] = np.arccos(np.clip(X['hz'] / X['h'], -1.0, 1.0))  # Clip to avoid invalid values
        X['i_deg'] = np.degrees(X['i'])  # Convert inclination to degrees

        # # Longitude of ascending node (Omega)
        n = np.cross([0, 0, 1], h)  # Cross product with the Z-axis to get the node vector
        n_mag = np.linalg.norm(n, axis=1)  # Magnitude of the node vector
        n_mag[n_mag == 0] = np.nan  # Replace zero magnitude with NaN

        X['Omega'] = np.arccos(np.clip(n[:, 0] / n_mag, -1.0, 1.0))
        X.loc[n[:, 1] < 0, 'Omega'] = 2 * np.pi - X.loc[n[:, 1] < 0, 'Omega']
        X['Omega_deg'] = np.degrees(X['Omega'])  # Convert Omega to degrees

        # # Argument of periapsis (omega)
        eccentricity_vec = np.array([X['ex'], X['ey'], X['ez']]).T
        omega = np.arccos(np.clip(np.sum(n * eccentricity_vec, axis=1) / (n_mag * X['e_mag']), -1.0, 1.0))
        X['omega'] = omega
        X.loc[X['ez'] < 0, 'omega'] = 2 * np.pi - X.loc[X['ez'] < 0, 'omega']  # Correct sign of omega
        X['omega_deg'] = np.degrees(X['omega'])  # Convert omega to degrees

        # True anomaly (nu)
        position_vec = np.array([X['x'] - X['centroid_x'], X['y'] - X['centroid_y'], X['z'] - X['centroid_z']]).T
        true_anomaly = np.arccos(np.clip(np.sum(eccentricity_vec * position_vec, axis=1) / (X['e_mag'] * X['r']), -1.0, 1.0))
        velocity_vec = np.array([X['vx'], X['vy'], X['vz']]).T
        X['nu'] = true_anomaly
        reverse_indices = np.sum(position_vec * velocity_vec, axis=1) < 0
        # X.loc[reverse_indices, 'nu'] = 2 * np.pi - X.loc[reverse_indices, 'nu']
        X['nu_deg'] = np.degrees(X['nu'])  # Convert nu to degrees

        # Calculate kinetic and potential energy
        X['kinetic_energy'] = 0.5 * X['mass'] * (X['vx']**2 + X['vy']**2 + X['vz']**2)
        X['potential_energy'] = -X['mass'] * X['centroid_mass'] / np.sqrt(X['rx']**2 + X['ry']**2 + X['rz']**2)

        # Calculate angular momentum and specific angular momentum
        X['angular_momentum'] = X['mass'] * (X['x'] * X['vy'] - X['y'] * X['vx'])
        X['specific_angular_momentum'] = X['angular_momentum'] / X['mass']

        # Additional features (adjust as needed)
        X['distance_to_centroid'] = np.sqrt(X['rx']**2 + X['ry']**2 + X['rz']**2)
        X['velocity_magnitude'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)


        # Semi-major axis (a)
        X['a'] = -X['mu'] / (2 * X['oe'])  # Semi-major axis formula from energy

        # Replace NaN and inf with valid defaults
        X = X.replace([np.inf, -np.inf], np.nan)  # Replace infinities with NaN
        X = X.fillna(0)  # Replace NaNs with zero or a meaningful default value



    return X, y


'''
def feature_engineering(X, y, is_orbital=True):
    if is_orbital:
        G = 6.67430e-11  # Gravitational constant

        # Calculate relative position and velocity of the planet with respect to the center
        X['r'] = np.sqrt((X['x'] - X['centroid_x'])**2 + 
                         (X['y'] - X['centroid_y'])**2 + 
                         (X['z'] - X['centroid_z'])**2)  # Distance from central body
        X['v'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)  # Speed of the planet

        # Avoid division by zero in 'r'
        # X['r'] = X['r'].replace(0, np.nan)  # Replace zero with NaN to avoid division errors
        
        # Gravitational parameter of the planet and central body
        X['mu'] = G * (X['mass'] + X['centroid_mass'])  # Gravitational parameter of the planet

        # Specific orbital energy (OE)
        X['oe'] = (X['v']**2) / 2 - X['mu'] / X['r']  # Orbital energy

        # Angular momentum components and magnitude
        X['hx'] = (X['y'] - X['centroid_y']) * X['vz'] - (X['z'] - X['centroid_z']) * X['vy']
        X['hy'] = (X['z'] - X['centroid_z']) * X['vx'] - (X['x'] - X['centroid_x']) * X['vz']
        X['hz'] = (X['x'] - X['centroid_x']) * X['vy'] - (X['y'] - X['centroid_y']) * X['vx']
        h = np.array([X['hx'], X['hy'], X['hz']]).T  # Ensure it's a 2D array, each row is a 3D vector
        X['h'] = np.linalg.norm(h, axis=1)  # Magnitude of angular momentum

        # Avoid division by zero in 'h'
        # X['h'] = X['h'].replace(0, np.nan)

        # Eccentricity vector components and magnitude
        X['ex'] = (X['hy'] * X['vz'] - X['hz'] * X['vy']) / X['mu'] - (X['x'] - X['centroid_x']) / X['r']
        X['ey'] = (X['hz'] * X['vx'] - X['hx'] * X['vz']) / X['mu'] - (X['y'] - X['centroid_y']) / X['r']
        X['ez'] = (X['hx'] * X['vy'] - X['hy'] * X['vx']) / X['mu'] - (X['z'] - X['centroid_z']) / X['r']
        X['e_mag'] = np.sqrt(X['ex']**2 + X['ey']**2 + X['ez']**2)  # Eccentricity magnitude

        # Ensure eccentricity is in a valid range [0, 1]
        X['e_mag'] = np.clip(X['e_mag'], 0, 1)

        # Inclination (i)
        X['i'] = np.arccos(np.clip(X['hz'] / X['h'], -1.0, 1.0))  # Clip to avoid invalid values

        # Longitude of ascending node (Omega)
        n = np.cross([0, 0, 1], h)  # Cross product with the Z-axis to get the node vector
        n_mag = np.linalg.norm(n, axis=1)  # Magnitude of the node vector
        n_mag[n_mag == 0] = np.nan  # Replace zero magnitude with NaN

        X['Omega'] = np.arccos(np.clip(n[:, 0] / n_mag, -1.0, 1.0))
        X.loc[n[:, 1] < 0, 'Omega'] = 2 * np.pi - X.loc[n[:, 1] < 0, 'Omega']

        # Argument of periapsis (omega)
        eccentricity_vec = np.array([X['ex'], X['ey'], X['ez']]).T
        omega = np.arccos(np.clip(np.sum(n * eccentricity_vec, axis=1) / (n_mag * X['e_mag']), -1.0, 1.0))
        X['omega'] = omega
        X.loc[X['ez'] < 0, 'omega'] = 2 * np.pi - X.loc[X['ez'] < 0, 'omega']

        # True anomaly (nu)
        position_vec = np.array([X['x'] - X['centroid_x'], X['y'] - X['centroid_y'], X['z'] - X['centroid_z']]).T
        eccentricity_vec = np.array([X['ex'], X['ey'], X['ez']]).T

        # Compute dot product for each row
        dot_product = np.sum(position_vec * eccentricity_vec, axis=1)
        X['nu'] = np.arccos(np.clip(dot_product / (X['r'] * X['e_mag']), -1.0, 1.0))
        # X.loc[dot_product < 0, 'nu'] = 2 * np.pi - X.loc[dot_product < 0, 'nu']

        # Semi-major axis (a)
        X['a'] = -X['mu'] / (2 * X['oe'])
        
    return X, y'''

'''
import numpy as np
import pandas as pd

def feature_engineering(X, y, is_orbital=True):
    G = 6.6743e-11  # Gravitational constant

    # Iterate through each row of X
    for idx, row in X.iterrows():
        # Extract relative position and velocity
        rx, ry, rz = row['x'] - row['centroid_x'], row['y'] - row['centroid_y'], row['z'] - row['centroid_z']
        X.loc[idx, 'rx'] = rx; X.loc[idx, 'ry'] = ry; X.loc[idx, 'rz'] = rz
        vx, vy, vz = row['vx'], row['vy'], row['vz']
        X.loc[idx, 'vx'] = vx; X.loc[idx, 'vy'] = vy; X.loc[idx, 'vz'] = vz
        r = np.sqrt(rx**2 + ry**2 + rz**2)
        X.loc[idx, 'r'] = r
        v = np.sqrt(vx**2 + vy**2 + vz**2)
        X.loc[idx, 'v'] = v

        # Calculate kinetic and potential energy
        X.loc[idx, 'kinetic_energy'] = 0.5 * X.loc[idx, 'mass'] * (X.loc[idx, 'vx']**2 + X.loc[idx, 'vy']**2 + X.loc[idx, 'vz']**2)
        X.loc[idx, 'potential_energy'] = -X.loc[idx, 'mass'] * X.loc[idx, 'centroid_mass'] / np.sqrt(X.loc[idx, 'rx']**2 + X.loc[idx, 'ry']**2 + X.loc[idx, 'rz']**2)

        # Calculate angular momentum and specific angular momentum
        X.loc[idx, 'angular_momentum'] = X.loc[idx, 'mass'] * (X.loc[idx, 'x'] * X.loc[idx, 'vy'] - X.loc[idx, 'y'] * X.loc[idx, 'vx'])
        X.loc[idx, 'specific_angular_momentum'] = X.loc[idx, 'angular_momentum'] / X.loc[idx, 'mass']

        # Additional features (adjust as needed)
        X.loc[idx, 'distance_to_centroid'] = np.sqrt(X.loc[idx, 'rx']**2 + X.loc[idx, 'ry']**2 + X.loc[idx, 'rz']**2)
        X.loc[idx, 'velocity_magnitude'] = np.sqrt(X.loc[idx, 'vx']**2 + X.loc[idx, 'vy']**2 + X.loc[idx, 'vz']**2)


        # Gravitational parameter (mu)
        mu = G * (row['mass'] + row['centroid_mass'])
        X.loc[idx, 'mu'] = mu

        # Specific orbital energy
        energy = (v**2) / 2 - mu / r
        X.loc[idx, 'oe'] = energy

        # Semi-major axis (a)
        a = -mu / (2 * energy)

        # Angular momentum vector
        h = np.cross([rx, ry, rz], [vx, vy, vz])
        X.loc[idx, 'hx'] = h[0]; X.loc[idx, 'hy'] = h[1]; X.loc[idx, 'hz'] = h[2]

        h_mag = np.linalg.norm(h)
        X.loc[idx, 'h_mag'] = h_mag

        # Eccentricity vector
        e_vec = (np.cross([vx, vy, vz], h) / mu) - np.array([rx, ry, rz]) / r
        X.loc[idx, 'ex'] = e_vec[0]; X.loc[idx, 'ey'] = e_vec[1]; X.loc[idx, 'ez'] = e_vec[2]
        e = np.linalg.norm(e_vec)

        # Inclination (i)
        i = np.arccos(h[2] / h_mag)

        # Node vector
        n = np.cross([0, 0, 1], h)
        X.loc[idx, 'nx'] = n[0]; X.loc[idx, 'ny'] = n[1]; X.loc[idx, 'nz'] = n[2]
        n_mag = np.linalg.norm(n)
        X.loc[idx, 'n_mag'] = n_mag

        # Longitude of ascending node (Omega)
        Omega = np.arccos(n[0] / n_mag) if n_mag != 0 else 0
        if n[1] < 0:
            Omega = 2 * np.pi - Omega

        # Argument of periapsis (omega)
        omega = np.arccos(np.dot(n, e_vec) / (n_mag * e)) if n_mag != 0 and e != 0 else 0
        if e_vec[2] < 0:
            omega = 2 * np.pi - omega

        # True anomaly (nu)
        nu = np.arccos(np.dot(e_vec, [rx, ry, rz]) / (e * r)) if e != 0 else 0
        if np.dot([rx, ry, rz], [vx, vy, vz]) < 0:
            nu = 2 * np.pi - nu
        X.loc[idx, 'nu'] = nu


    return X, y
'''
'''
import numpy as np
import pandas as pd

def feature_engineering(df, y, is_orbital=True):
    """
    Enhanced orbital mechanics feature engineering with improved numerical stability
    and proper DataFrame handling.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Input data with position, velocity, and mass information
    y : pandas DataFrame
        Target orbital elements
    is_orbital : bool
        Flag for computing orbital features
        
    Returns:
    --------
    features_df : pandas DataFrame
        New DataFrame with engineered features
    y : pandas DataFrame
        Unchanged target variables
    """
    # Create a new DataFrame to avoid the SettingWithCopyWarning
    X = df.copy()
    
    # Physical constants
    G = 6.6743e-11  # Gravitational constant in m^3 kg^-1 s^-2
    eps = 1e-15     # Numerical stability epsilon
    
    # Basic position and velocity features
    relative_pos = {
        'rx': X['x'] - X['centroid_x'],
        'ry': X['y'] - X['centroid_y'],
        'rz': X['z'] - X['centroid_z']
    }
    
    for key, value in relative_pos.items():
        X[key] = value
    
    # Magnitudes with numerical stability
    r = np.sqrt(relative_pos['rx']**2 + relative_pos['ry']**2 + relative_pos['rz']**2 + eps)
    v = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2 + eps)
    X['r'] = r
    X['v'] = v
    
    # Gravitational parameter
    X['mu'] = G * (X['mass'] + X['centroid_mass'])
    # Calculate mass ratio features
    X['mass_ratio'] = X['mass'] / X['centroid_mass']
    # Energy calculations
    X['v_squared'] = X['v']**2
    X['kinetic_energy'] = 0.5 * X['mass'] * X['v_squared']
    X['potential_energy'] = -G * X['mass'] * X['centroid_mass'] / X['r']
    X['total_energy'] = X['kinetic_energy'] + X['potential_energy']
    X['specific_energy'] = X['total_energy'] / (X['mass'] + eps)
    
    # Angular momentum calculations
    h_components = {
        'hx': X['ry'] * X['vz'] - X['rz'] * X['vy'],
        'hy': X['rz'] * X['vx'] - X['rx'] * X['vz'],
        'hz': X['rx'] * X['vy'] - X['ry'] * X['vx']
    }
    
    for key, value in h_components.items():
        X[key] = value
    
    X['h_mag'] = np.sqrt(h_components['hx']**2 + h_components['hy']**2 + h_components['hz']**2 + eps)
    
    if is_orbital:
        # Velocity and position dot product
        v_dot_r = (X['vx'] * X['rx'] + X['vy'] * X['ry'] + X['vz'] * X['rz'])
        X['v_dot_r'] = v_dot_r
        
        # Normalized vectors for better numerical stability
        for comp in ['x', 'y', 'z']:
            X[f'r_norm_{comp}'] = X[f'r{comp}'] / X['r']
            X[f'v_norm_{comp}'] = X[f'v{comp}'] / X['v']
        
        # Eccentricity vector with improved stability
        for comp in ['x', 'y', 'z']:
            X[f'e{comp}'] = ((X['v_squared'] * X[f'r{comp}'] - v_dot_r * X[f'v{comp}']) / 
                            (X['mu'] + eps) - X[f'r{comp}'] / X['r'])
        
        X['eccentricity'] = np.sqrt(X['ex']**2 + X['ey']**2 + X['ez']**2 + eps)
        
        # Node vector with improved handling
        X['nx'] = -h_components['hy']
        X['ny'] = h_components['hx']
        X['nz'] = np.zeros_like(X['nx'])
        X['n_mag'] = np.sqrt(X['nx']**2 + X['ny']**2 + eps)
        
        # Orbital elements with enhanced stability
        # Inclination with safe division
        h_mag_safe = np.maximum(X['h_mag'], eps)
        X['inclination'] = np.arccos(np.clip(X['hz'] / h_mag_safe, -1.0, 1.0))
        
        # Longitude of ascending node
        n_mag_safe = np.maximum(X['n_mag'], eps)
        nx_normalized = np.clip(X['nx'] / n_mag_safe, -1.0, 1.0)
        X['longitude_ascending_node'] = np.where(
            X['ny'] >= 0,
            np.arccos(nx_normalized),
            2 * np.pi - np.arccos(nx_normalized)
        )
        
        # Argument of periapsis
        n_dot_e = X['nx'] * X['ex'] + X['ny'] * X['ey']
        ne_product = X['n_mag'] * X['eccentricity']
        ne_safe = np.maximum(ne_product, eps)
        X['argument_periapsis'] = np.where(
            X['ez'] >= 0,
            np.arccos(np.clip(n_dot_e / ne_safe, -1.0, 1.0)),
            2 * np.pi - np.arccos(np.clip(n_dot_e / ne_safe, -1.0, 1.0))
        )
        
        # True anomaly with improved stability
        e_dot_r = X['ex'] * X['rx'] + X['ey'] * X['ry'] + X['ez'] * X['rz']
        er_product = X['eccentricity'] * X['r']
        er_safe = np.maximum(er_product, eps)
        cos_nu = np.clip(e_dot_r / er_safe, -1.0, 1.0)
        
        # Enhanced true anomaly calculation
        X['true_anomaly'] = np.where(
            X['eccentricity'] > eps,
            np.where(v_dot_r >= 0,
                    np.arccos(cos_nu),
                    2 * np.pi - np.arccos(cos_nu)),
            np.arctan2(X['ry'], X['rx'])  # For circular orbits
        )
        
        # Additional features for better prediction
        X['specific_angular_momentum'] = X['h_mag'] / (X['mass'] + eps)
        X['orbital_period'] = 2 * np.pi * np.sqrt(np.abs(X['r']**3 / (X['mu'] + eps)))
        X['mean_motion'] = 2 * np.pi / (X['orbital_period'] + eps)
        
        # Convert angles to degrees
        for angle in ['inclination', 'longitude_ascending_node', 'argument_periapsis', 'true_anomaly']:
            X[f'{angle}_deg'] = np.rad2deg(X[angle])
            
    return X, y'''

'''
def feature_engineering(X, y):
    """
    Perform feature engineering to calculate orbital features.
    
    Args:
        X (pd.DataFrame): DataFrame containing the planet's features.
        
    Returns:
        pd.DataFrame: Updated DataFrame with additional features.
    """
    G = 6.67430e-11  # Gravitational constant

    # Relative position and velocity
    X['rx'] = X['x'] - X['centroid_x']
    X['ry'] = X['y'] - X['centroid_y']
    X['rz'] = X['z'] - X['centroid_z']
    X['r'] = np.sqrt(X['rx']**2 + X['ry']**2 + X['rz']**2)

    X['v'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)

    # Gravitational parameter (mu)
    X['mu'] = G * (X['mass'] + X['centroid_mass'])

    # Orbital energy (specific energy)
    X['oe'] = (X['v']**2) / 2 - X['mu'] / X['r']

    # Angular momentum components and magnitude
    X['hx'] = X['ry'] * X['vz'] - X['rz'] * X['vy']
    X['hy'] = X['rz'] * X['vx'] - X['rx'] * X['vz']
    X['hz'] = X['rx'] * X['vy'] - X['ry'] * X['vx']
    X['h'] = np.sqrt(X['hx']**2 + X['hy']**2 + X['hz']**2)

    # Eccentricity vector and magnitude
    X['ex'] = (X['vy'] * X['hz'] - X['vz'] * X['hy']) / X['mu'] - X['rx'] / X['r']
    X['ey'] = (X['vz'] * X['hx'] - X['vx'] * X['hz']) / X['mu'] - X['ry'] / X['r']
    X['ez'] = (X['vx'] * X['hy'] - X['vy'] * X['hx']) / X['mu'] - X['rz'] / X['r']
    X['e_mag'] = np.sqrt(X['ex']**2 + X['ey']**2 + X['ez']**2)

    # Inclination
    X['i'] = np.arccos(np.clip(X['hz'] / X['h'], -1.0, 1.0))

    # Node vector and longitude of ascending node
    X['nx'] = -X['hy']
    X['ny'] = X['hx']
    X['n_mag'] = np.sqrt(X['nx']**2 + X['ny']**2)
    X['Omega'] = np.arccos(np.clip(X['nx'] / X['n_mag'], -1.0, 1.0))
    X.loc[X['ny'] < 0, 'Omega'] = 2 * np.pi - X.loc[X['ny'] < 0, 'Omega']

    # Argument of periapsis
    e_vec = np.array([X['ex'], X['ey'], X['ez']]).T
    n_vec = np.array([X['nx'], X['ny'], np.zeros(len(X))]).T
    X['omega'] = np.arccos(np.clip(np.sum(e_vec * n_vec, axis=1) / (X['e_mag'] * X['n_mag']), -1.0, 1.0))
    X.loc[X['ez'] < 0, 'omega'] = 2 * np.pi - X.loc[X['ez'] < 0, 'omega']

    # True anomaly
    r_vec = np.array([X['rx'], X['ry'], X['rz']]).T
    v_vec = np.array([X['vx'], X['vy'], X['vz']]).T
    X['nu'] = np.arccos(np.clip(np.sum(e_vec * r_vec, axis=1) / (X['e_mag'] * X['r']), -1.0, 1.0))
    X.loc[np.sum(r_vec * v_vec, axis=1) < 0, 'nu'] = 2 * np.pi - X.loc[np.sum(r_vec * v_vec, axis=1) < 0, 'nu']

    # Semi-major axis
    X['a'] = -X['mu'] / (2 * X['oe'])

    # Sine and cosine transformations for cyclical features
    X['sin_nu'] = np.sin(X['nu'])
    X['cos_nu'] = np.cos(X['nu'])

    return X, y
'''

# def run_models(X, y):
#     feature_engineering(X, y)
#     # # Impute missing values with mean
#     # imputer = SimpleImputer(strategy='mean')  # Choose 'median' or another strategy if needed
#     # X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
#     # y = pd.DataFrame(imputer.fit_transform(y), columns=y.columns)

#     # Train/test split
#     print("+------------------+------------------------------------------++")
#     print("| Train-Test-Split |------------------------------------------||")
#     print("+------------------+------------------------------------------++")
    
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=33)
#     print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")

#     # 1. Support Vector Regression (SVR)
#     print("+---------------------------------+---------------------------++")
#     print("| Support Vector Regression (SVR) |---------------------------||")
#     print("+---------------------------------+---------------------------++")
#     svr = SVR(kernel='poly', degree=5, C=10, epsilon=0.1, gamma='scale')
#     mor_svr = MultiOutputRegressor(svr)
#     mor_svr.fit(X_train, y_train)
#     y_pred_svr = mor_svr.predict(X_test)
#     evaluate_model("SVR", y_test, y_pred_svr)

#     # 2. Gradient Boosting Regressor
#     print("+-----------------------------------+-------------------------++")
#     print("| Gradient Boosting Regressor (GBR) |-------------------------||")
#     print("+-----------------------------------+-------------------------++")
#     gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)
#     mor_gbr = MultiOutputRegressor(gbr)
#     mor_gbr.fit(X_train, y_train)
#     y_pred_gbr = mor_gbr.predict(X_test)
#     evaluate_model("Gradient Boosting", y_test, y_pred_gbr)

#     # 3. Xtrem Gradient Boosting Regressor
#     print("+-----------------------------------------+-------------------++")
#     print("| Xtrem Gradient Boosting Regressor (GBR) |-------------------||")
#     print("+-----------------------------------------+-------------------++")
#     xgbr = XGBRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)
#     mor_gbr = MultiOutputRegressor(xgbr)
#     mor_gbr.fit(X_train, y_train)
#     y_pred_gbr = mor_gbr.predict(X_test)
#     evaluate_model("Gradient Boosting", y_test, y_pred_gbr)


#     # 4. SGD Regressor
#     print("+---------------------+---------------------------------------++")
#     print("| SGD Regressor (GBR) |---------------------------------------||")
#     print("+---------------------+---------------------------------------++")
#     lgb_model = SGDRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)
#     mor_gbr = MultiOutputRegressor(lgb_model)
#     mor_gbr.fit(X_train, y_train)
#     y_pred_gbr = mor_gbr.predict(X_test)
#     evaluate_model("Gradient Boosting", y_test, y_pred_gbr)

#     # 5. Random Forest Regressor
#     print("+-------------------------------+-----------------------------++")
#     print("| Random Forest Regressor (RFR) |-----------------------------||")
#     print("+-------------------------------+-----------------------------++")
#     rfr = RandomForestRegressor(n_estimators=200, max_depth=20, random_state=33)
#     mor_rfr = MultiOutputRegressor(rfr)
#     mor_rfr.fit(X_train, y_train)
#     y_pred_rfr = mor_rfr.predict(X_test)
#     evaluate_model("Random Forest", y_test, y_pred_rfr)

#     # 6. Ensemble Voting Regressor
#     print("+---------------------------------+--------------------------++")
#     print("| Ensemble Voting Regressor (EVR) |--------------------------||")
#     print("+---------------------------------+--------------------------++")
#     voting_regressor = VotingRegressor(
#         estimators=[
#             ('gbr', GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=33)),
#             ('rfr', RandomForestRegressor(n_estimators=200, max_depth=10, random_state=33)),
#             ('svr', SVR(kernel='rbf', C=10, epsilon=0.1, gamma='scale'))
#         ]
#     )
#     mor_voting = MultiOutputRegressor(voting_regressor)
#     mor_voting.fit(X_train, y_train)
#     y_pred_voting = mor_voting.predict(X_test)
#     evaluate_model("Voting Regressor", y_test, y_pred_voting)
#     # Save the trained model to a file
#     joblib.dump(mor_svr, 'save_models/svr_model.joblib')
#     joblib.dump(mor_gbr, 'save_models/gbr_model.joblib')
#     joblib.dump(mor_rfr, 'save_models/rfr_model.joblib')
#     joblib.dump(mor_voting, 'save_models/voting_regressor_model.joblib')

#     print("Models saved successfully.")


def run_models(X, y):
    X, y = feature_engineering(X, y)
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)
    y = imputer.fit_transform(y)

    feature_scaler = StandardScaler()
    target_scaler = StandardScaler()
    
    X = feature_scaler.fit_transform(X)
    y = target_scaler.fit_transform(y)

    # Grid Search Hyper Tuning
    param_grid = {
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'n_estimators': [100, 200],
        # 'subsample': [0.8, 0.9, 1.0],
        'subsample': [0.8,],
        'colsample_bytree': [0.8],
        # 'gamma': [0, 0.1, 0.2]  # Regularization parameter
    }

    # Train/test split
    print("+------------------+------------------------------------------++")
    print("| Train-Test-Split |------------------------------------------||")
    print("+------------------+------------------------------------------++")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=33)
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")

    # 1. Support Vector Regression (SVR)
    print("+---------------------------------+---------------------------++")
    print("| Support Vector Regression (SVR) |---------------------------||")
    print("+---------------------------------+---------------------------++")
    svr = SVR(kernel='poly', degree=5, C=2, epsilon=0.2, gamma='scale')
    mor_svr = MultiOutputRegressor(svr)
    mor_svr.fit(X_train, y_train)
    y_pred_svr = mor_svr.predict(X_test)
    evaluate_model("SVR", y_test, y_pred_svr)

    # 2. Gradient Boosting Regressor
    print("+-----------------------------------+-------------------------++")
    print("| Gradient Boosting Regressor (GBR) |-------------------------||")
    print("+-----------------------------------+-------------------------++")
    gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)
    mor_gbr = MultiOutputRegressor(gbr)
    mor_gbr.fit(X_train, y_train)
    y_pred_gbr = mor_gbr.predict(X_test)
    evaluate_model("Gradient Boosting", y_test, y_pred_gbr)

    # 3. Xtreme Gradient Boosting Regressor (XGBR)
    print("+-------------------------------------------+-----------------++")
    print("| Xtreme Gradient Boosting Regressor (XGBR) |-----------------||")
    print("+-------------------------------------------+-----------------++")
    # xgbr = XGBRegressor(n_estimators=120, learning_rate=0.07, max_depth=4, random_state=33)
    # grid_search = GridSearchCV(XGBRegressor(random_state=42), param_grid, scoring='r2', cv=5)
    # mor_xgbr = MultiOutputRegressor(grid_search)
    # # mor_xgbr = MultiOutputRegressor(xgbr)
    # # Train the model with grid search
    # mor_xgbr.fit(X_train, y_train)
    # y_pred_xgbr = mor_xgbr.predict(X_test)
    # evaluate_model("XGBoost", y_test, y_pred_xgbr)

    # Initialize GridSearchCV with XGBRegressor
    base_xgbr = XGBRegressor(random_state=42)
    grid_search = GridSearchCV(base_xgbr, param_grid, scoring='r2', cv=5)

    # Perform GridSearchCV for each target variable independently
    best_models = []
    for i in range(y_train.shape[1]):
        print(f"Grid search for target {i + 1}/{y_train.shape[1]}...")
        grid_search.fit(X_train, y_train[:, i])
        best_models.append(grid_search.best_estimator_)
    
    # Create a MultiOutputRegressor using the best models from GridSearchCV
    mor_xgbr = MultiOutputRegressor(estimator=base_xgbr)
    mor_xgbr.estimators_ = best_models  # Manually set the best estimators
    y_pred_xgbr = mor_xgbr.predict(X_test)

    evaluate_model("XGBoost", y_test, y_pred_xgbr)



    # 5. Random Forest Regressor (RFR)
    print("+-------------------------------+-----------------------------++")
    print("| Random Forest Regressor (RFR) |-----------------------------||")
    print("+-------------------------------+-----------------------------++")
    rfr = RandomForestRegressor(n_estimators=300, max_depth=10, random_state=33)
    mor_rfr = MultiOutputRegressor(rfr)
    mor_rfr.fit(X_train, y_train)
    y_pred_rfr = mor_rfr.predict(X_test)
    evaluate_model("Random Forest", y_test, y_pred_rfr)

    # 6. Ensemble Voting Regressor (EVR)
    print("+---------------------------------+--------------------------++")
    print("| Ensemble Voting Regressor (EVR) |--------------------------||")
    print("+---------------------------------+--------------------------++")
    voting_regressor = VotingRegressor(
        estimators=[
            ('gbr', GradientBoostingRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)),
            ('rfr', RandomForestRegressor(n_estimators=300, max_depth=10, random_state=11)),
            ('svr', SVR(kernel='rbf', C=10, epsilon=0.2, gamma='scale'))
        ]
    )
    mor_voting = MultiOutputRegressor(voting_regressor)
    mor_voting.fit(X_train, y_train)
    y_pred_voting = mor_voting.predict(X_test)
    evaluate_model("Voting Regressor", y_test, y_pred_voting)

    # Save the trained models
    joblib.dump(mor_svr, 'save_models/svr_model.joblib')
    joblib.dump(mor_gbr, 'save_models/gbr_model.joblib')
    joblib.dump(mor_xgbr, 'save_models/xgbr_model.joblib')
    joblib.dump(mor_rfr, 'save_models/rfr_model.joblib')
    joblib.dump(mor_voting, 'save_models/voting_regressor_model.joblib')

    print("Models saved successfully.")


# # =========================================

# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.preprocessing import StandardScaler
# from xgboost import XGBRegressor
# from sklearn.metrics import r2_score

# # Load the dataset
# file_path = '/content/drive/MyDrive/ML_Project/updated_training_data.xlsx - Sheet1.csv'
# data = pd.read_csv(file_path)

# # Define feature and target columns
# features = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'mass']
# target = 'pl_orblper'

# # Prepare feature matrix (X) and target column (y)
# X = data[features]
# y = data[target]

# # Handle NaN values
# X.fillna(X.mean(), inplace=True)
# y.fillna(y.mean(), inplace=True)

# # Handle infinite values
# X.replace([np.inf, -np.inf], 1e10, inplace=True)
# y.replace([np.inf, -np.inf], 1e10, inplace=True)

# # Remove outliers using IQR method
# def remove_outliers_iqr(data):
#     Q1 = data.quantile(0.25)
#     Q3 = data.quantile(0.75)
#     IQR = Q3 - Q1
#     return data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]

# # Combine X and y for outlier detection
# data_combined = pd.concat([X, y], axis=1)
# data_cleaned = remove_outliers_iqr(data_combined)

# # Separate the cleaned data back into X and y
# X_cleaned = data_cleaned[features]
# y_cleaned = data_cleaned[target]

# # Apply log transformation if all values are positive
# if (y_cleaned > 0).all():
#     y_transformed = np.log(y_cleaned + 1)
# else:
#     y_transformed = y_cleaned

# # Scale the features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X_cleaned)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_transformed, test_size=0.2, random_state=42)

# # Define the parameter grid for hyperparameter tuning
# param_grid = {
#     'learning_rate': [0.01, 0.1, 0.2],
#     'max_depth': [3, 5, 7],
#     'n_estimators': [100, 200],
#     'subsample': [0.8, 0.9, 1.0],
#     'colsample_bytree': [0.8, 1.0],
#     'gamma': [0, 0.1, 0.2]  # Regularization parameter
# }

# # Initialize the GridSearchCV
# grid_search = GridSearchCV(XGBRegressor(random_state=42), param_grid, scoring='r2', cv=5)

# # Train the model with grid search
# grid_search.fit(X_train, y_train)

# # Get the best model
# best_model = grid_search.best_estimator_

# # Predict on the test set
# y_pred_transformed = best_model.predict(X_test)

# # Inverse log transformation
# if (y_cleaned > 0).all():
#     y_pred = np.exp(y_pred_transformed) - 1
# else:
#     y_pred = y_pred_transformed

# # Evaluate the model with R² score
# final_r2 = r2_score(y_test, y_pred)

# # Print the final evaluation
# print(f"Best Hyperparameters: {grid_search.best_params_}")
# print(f"R² Score for pl_orblper: {final_r2}")

# # =========================================


def evaluate_model(model_name, y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
    r2 = r2_score(y_test, y_pred, multioutput='uniform_average')
    print(f"{model_name} - Mean Squared Error (MSE): {mse:.4f}")
    print(f"{model_name} - R² Score: {r2:.4f}")
    # Evaluate individual R² scores
    individual_r2 = r2_score(y_test, y_pred, multioutput='raw_values')
    for i, r2 in enumerate(individual_r2):
        print(f"{model_name} - R² for target {y.columns[i]}: {round(r2 * 100, 4)}%")

def load_model():
    # Load the saved model from the file
    mor_svr = joblib.load('save_models/rfr_model.joblib')
    return mor_svr

if __name__ == "__main__":
    list_of_dataframe = version_2()
    list_of_dataframe[0].to_csv('data.csv', index=False)
    X, y = version_4_2(list_of_dataframe)
    run_models(X, y)