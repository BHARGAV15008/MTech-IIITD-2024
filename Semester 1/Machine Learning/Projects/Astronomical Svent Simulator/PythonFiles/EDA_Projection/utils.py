import numpy as np
import pandas as pd
import math

def lcm(a: float, b: float) -> float:
    """
    Calculate the Least Common Multiple (LCM) of two numbers.

    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: Least Common Multiple of a and b.
    """
    return abs(a * b) // math.gcd(int(a), int(b))


def get_lcm_of_orbits(planetary_data: pd.DataFrame) -> float:
    """
    Calculate the LCM of the orbital periods of planets in the dataset.

    Args:
        planetary_data (pd.DataFrame): DataFrame containing 'pl_orbper' column.

    Returns:
        float: LCM of the orbital periods.
    """
    periods = planetary_data['pl_orbper'].tolist()
    lcm_value = periods[0]
    for period in periods[1:]:
        lcm_value = lcm(lcm_value, period)
    return lcm_value


import numpy as np

def kepler_solver(mean_anomaly: float, eccentricity: float, tolerance: float = 1e-6, max_iterations: int = 100) -> float:
    """
    Solve Kepler's equation for the eccentric anomaly using iterative numerical methods.

    Args:
        mean_anomaly (float): Mean anomaly (M) in radians, between 0 and 2π.
        eccentricity (float): Eccentricity of the orbit (0 <= e < 1 for elliptical orbits).
        tolerance (float): Tolerance for convergence (default: 1e-6).
        max_iterations (int): Maximum number of iterations to prevent infinite loops.

    Returns:
        float: Eccentric anomaly (E) in radians.

    Raises:
        ValueError: If the solver does not converge within the allowed iterations.
    """
    # Normalize mean anomaly to be within [0, 2π]
    mean_anomaly = mean_anomaly % (2 * np.pi)
    
    # Initial guess for Eccentric Anomaly
    if eccentricity < 0.8:
        E = mean_anomaly  # Good initial guess for low eccentricity
    else:
        E = np.pi  # For higher eccentricity, start at π

    iteration = 0

    while iteration < max_iterations:
        # Update step for eccentric anomaly
        delta_E = (E - eccentricity * np.sin(E) - mean_anomaly) / (1 - eccentricity * np.cos(E))
        E -= delta_E
        
        # Check for convergence
        if abs(delta_E) < tolerance:
            return E
        
        iteration += 1

    raise ValueError("Kepler solver did not converge within the maximum allowed iterations.")

def get_true_anomaly(mean_anomaly: float, eccentricity: float) -> float:
    """
    Calculate the true anomaly (v) from the mean anomaly (M) and eccentricity (e).

    Args:
        mean_anomaly (float): Mean anomaly (M) in radians.
        eccentricity (float): Eccentricity of the orbit.

    Returns:
        float: True anomaly (v) in radians.
    """
    # Solve Kepler's equation for the eccentric anomaly (E)
    E = kepler_solver(mean_anomaly, eccentricity)
    
    # Convert eccentric anomaly (E) to true anomaly (v)
    sin_v = np.sqrt(1 - eccentricity**2) * np.sin(E) / (1 - eccentricity * np.cos(E))
    cos_v = (np.cos(E) - eccentricity) / (1 - eccentricity * np.cos(E))
    true_anomaly = np.arctan2(sin_v, cos_v)
    
    return true_anomaly




# def kepler_solver(mean_anomaly: float, eccentricity: float, tolerance: float = 1e-6, max_iterations: int = 100) -> float:
#     """
#     Solve Kepler's equation for the eccentric anomaly using iterative numerical methods.

#     Args:
#         mean_anomaly (float): Mean anomaly (M) in radians, between 0 and 2π.
#         eccentricity (float): Eccentricity of the orbit (0 <= e < 1 for elliptical orbits).
#         tolerance (float): Tolerance for convergence (default: 1e-6).
#         max_iterations (int): Maximum number of iterations to prevent infinite loops.

#     Returns:
#         float: Eccentric anomaly (E) in radians.

#     Raises:
#         ValueError: If the solver does not converge within the allowed iterations.
#     """
#     E = mean_anomaly  # Initial guess for Eccentric Anomaly
#     iteration = 0

#     while iteration < max_iterations:
#         delta_E = (E - eccentricity * np.sin(E) - mean_anomaly) / (1 - eccentricity * np.cos(E))
#         E -= delta_E
        
#         if abs(delta_E) < tolerance:
#             return E
        
#         iteration += 1

#     raise ValueError("Kepler solver did not converge within the maximum allowed iterations.")

# def get_true_anomaly(mean_anomaly: float, eccentricity: float) -> float:
#     """
#     Calculate the true anomaly (v) from the mean anomaly (M) and eccentricity (e).

#     Args:
#         mean_anomaly (float): Mean anomaly (M) in radians.
#         eccentricity (float): Eccentricity of the orbit.

#     Returns:
#         float: True anomaly (v) in radians.
#     """
#     # Solve Kepler's equation for the eccentric anomaly (E)
#     E = kepler_solver(mean_anomaly, eccentricity)
    
#     # Convert eccentric anomaly (E) to true anomaly (v)
#     true_anomaly = 2 * np.arctan2(
#         np.sqrt(1 + eccentricity) * np.sin(E / 2),
#         np.sqrt(1 - eccentricity) * np.cos(E / 2)
#     )
    
#     return true_anomaly

# def solve_kepler(M: float, e: float, tol: float = 1e-6) -> float:
#     """
#     Solve Kepler's equation for the eccentric anomaly (E).

#     Args:
#         M (float): Mean anomaly in radians.
#         e (float): Eccentricity of the orbit.
#         tol (float): Tolerance for convergence.

#     Returns:
#         float: Eccentric anomaly (E) in radians.
#     """
#     E = M
#     while True:
#         delta_E = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
#         E -= delta_E
#         if abs(delta_E) < tol:
#             break
#     return E


# def large_omega(data: pd.DataFrame) -> pd.DataFrame:
#     """
#     Calculate the Longitude of the Ascending Node (Ω) for planets in the dataset
#     and add it as a new column to the DataFrame.
    
#     Args:
#         data (pd.DataFrame): Input DataFrame containing 'ra', 'dec', and 'pl_orbincl'.
    
#     Returns:
#         pd.DataFrame: Updated DataFrame with 'omega_capital_deg' (Ω in degrees) column added.
#     """
#     required_columns = ['ra', 'dec', 'pl_orbincl']
#     if not all(col in data.columns for col in required_columns):
#         raise ValueError(f"The dataset must contain the columns: {required_columns}")
    
#     data['ra_rad'] = np.radians(data['ra'])
#     data['dec_rad'] = np.radians(data['dec'])
#     data['incl_rad'] = np.radians(data['pl_orbincl'])

#     reference_ra = 0
#     reference_dec = 0

#     data['longitude_of_ascending_node'] = np.arctan2(
#         np.cos(reference_dec) * np.sin(data['ra_rad'] - reference_ra),
#         np.cos(data['incl_rad']) * np.sin(reference_dec) -
#         np.sin(data['incl_rad']) * np.cos(reference_dec) * np.cos(data['ra_rad'] - reference_ra)
#     )

#     data['pl_Omega'] = np.degrees(data['longitude_of_ascending_node']) % 360

#     data.drop(['ra_rad', 'dec_rad', 'incl_rad', 'longitude_of_ascending_node'], axis=1, inplace=True)

#     return data

def large_omega(data: pd.DataFrame, reference_ra: float = 0, reference_dec: float = 0) -> pd.DataFrame:
    """
    Calculate the Longitude of the Ascending Node (Ω) for planets in the dataset
    and add it as a new column to the DataFrame.
    
    Args:
        data (pd.DataFrame): Input DataFrame containing 'ra', 'dec', and 'pl_orbincl'.
        reference_ra (float): Reference right ascension (in degrees, default is 0).
        reference_dec (float): Reference declination (in degrees, default is 0).
    
    Returns:
        pd.DataFrame: Updated DataFrame with 'pl_Omega' (Ω in degrees) column added.
    """
    # Required columns check
    required_columns = ['ra', 'dec', 'pl_orbincl']
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"The dataset must contain the columns: {required_columns}")

    # Handle missing or non-numeric values
    data['ra'] = pd.to_numeric(data['ra'], errors='coerce')
    data['dec'] = pd.to_numeric(data['dec'], errors='coerce')
    data['pl_orbincl'] = pd.to_numeric(data['pl_orbincl'], errors='coerce')
    data = data.dropna(subset=required_columns)

    # Convert to radians
    data['ra_rad'] = np.radians(data['ra'])
    data['dec_rad'] = np.radians(data['dec'])
    data['incl_rad'] = np.radians(data['pl_orbincl'])

    # Reference values in radians
    reference_ra_rad = np.radians(reference_ra)
    reference_dec_rad = np.radians(reference_dec)

    # Calculate the longitude of the ascending node
    data['longitude_of_ascending_node'] = np.arctan2(
        np.cos(reference_dec_rad) * np.sin(data['ra_rad'] - reference_ra_rad),
        np.cos(data['incl_rad']) * np.sin(reference_dec_rad) -
        np.sin(data['incl_rad']) * np.cos(reference_dec_rad) * np.cos(data['ra_rad'] - reference_ra_rad)
    )

    # Convert to degrees and normalize to [0, 360)
    data['pl_Omega'] = np.degrees(data['longitude_of_ascending_node']) % 360

    # Drop intermediate columns
    data.drop(['ra_rad', 'dec_rad', 'incl_rad', 'longitude_of_ascending_node'], axis=1, inplace=True)

    return data


def simulate_orbit_step(a: float, e: float, i: float, omega: float, Omega: float, P: float, time: float) -> np.ndarray:
    """
    Simulate the position of an orbiting body at a given time.

    Args:
        a (float): Semi-major axis of the orbit.
        e (float): Eccentricity of the orbit.
        i (float): Inclination of the orbit in degrees.
        omega (float): Argument of periapsis in degrees.
        Omega (float): Longitude of ascending node in degrees.
        P (float): Orbital period in time units.
        time (float): Time elapsed since periapsis passage.

    Returns:
        np.ndarray: 3D coordinates (x, y, z) of the orbiting body.
    """
    # Calculate the mean anomaly
    M = 2 * np.pi * (time % P) / P  
    
    # Convert angles from degrees to radians
    i_rad = np.radians(i) 
    omega_rad = np.radians(omega) 
    Omega_rad = np.radians(Omega) 
    
    # Solve Kepler's equation to find the eccentric anomaly
    E = kepler_solver(M, e) 
    
    # Calculate the true anomaly
    true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)) 
    
    # Calculate the radius
    r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly)) 
    
    # Calculate the orbital coordinates in the orbital plane
    x_orb = r * np.cos(true_anomaly) 
    y_orb = r * np.sin(true_anomaly) 
    z_orb = 0  
    
    # Rotation matrices for the orbital transformations
    R_i = np.array([[1, 0, 0], 
                    [0, np.cos(i_rad), -np.sin(i_rad)], 
                    [0, np.sin(i_rad), np.cos(i_rad)]]) 
    
    R_omega = np.array([[np.cos(omega_rad), -np.sin(omega_rad), 0], 
                        [np.sin(omega_rad), np.cos(omega_rad), 0], 
                        [0, 0, 1]]) 
    
    R_Omega = np.array([[np.cos(Omega_rad), -np.sin(Omega_rad), 0], 
                        [np.sin(Omega_rad), np.cos(Omega_rad), 0], 
                        [0, 0, 1]]) 
    
    # Combine the rotation matrices
    rotation_matrix = R_Omega @ R_i @ R_omega 
    
    # Calculate the final orbital coordinates in 3D space
    orbital_coords = np.dot(rotation_matrix, np.array([x_orb, y_orb, z_orb])) 
    
    return orbital_coords


def calculate_important_parameters(data: pd.DataFrame) -> pd.DataFrame: # type: ignore
    """
    Calculate important parameters for the dataset.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with important parameters.
    """

    # Let determined and calculate inital parameters: intial position, velocity
    required_columns = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_Omega', 'pl_orbper']
    

    for idx, planet in data.iterrows():
        if not all(pd.notnull(planet[col]) for col in required_columns):
            continue
        
        # t = np.linspace(0, 2 * np.pi, 1)  # Full orbit in radians
        t = np.linspace(0, 2 * np.pi, 100);rand_index=np.random.randint(0,99);
        # Pre-compute the full orbital path
        # Pre-compute planet velocity
        vx_orbit, vy_orbit, vz_orbit = compute_orbit_velocity(
            a=planet['pl_orbsmax'],
            e=planet['pl_orbeccen'],
            i=np.radians(planet['pl_orbincl']),
            omega=np.radians(planet['pl_orblper']),
            Omega=np.radians(planet['pl_Omega']),
            # t = t
            t = t[0]  #t[rand_index]
        )
        # yield vx_orbit ,vy_orbit ,vz_orbit

        # Pre-compute planet position
        x_orbit, y_orbit, z_orbit = compute_orbit_path(
            a=planet['pl_orbsmax'],
            e=planet['pl_orbeccen'],
            i=np.radians(planet['pl_orbincl']),
            omega=np.radians(planet['pl_orblper']),
            Omega=np.radians(planet['pl_Omega']),
            # t = t
            t = t[0]  #t[rand_index]
        )
        # yield x_orbit ,y_orbit ,z_orbit
        print("type of vx_orbit",type(vx_orbit))
        data.loc[idx, 'vx'] = round(vx_orbit, 5)
        data.loc[idx, 'vy'] = round(vy_orbit, 5)
        data.loc[idx, 'vz'] = round(vz_orbit, 5)
        data.loc[idx, 'x'] = round(x_orbit, 5)
        data.loc[idx, 'y'] = round(y_orbit, 5)
        data.loc[idx, 'z'] = round(z_orbit, 5)

    # Set threshold mass ratio
    threshold_mass_ratio = 0.01
    store_max_mass_ratio = {}

    # Calculate mass ratio of planets and stars
    for i, planet in data.iterrows():
        for j, other_planet in data.iterrows():
            if planet['pl_name'] != other_planet['pl_name'] and planet['pl_bmasse'] != 0 and other_planet['pl_bmasse'] != 0:
                # Calculate mass ratio
                if planet['pl_bmasse'] < other_planet['pl_bmasse']:
                    mass_ratio = round((planet['pl_bmasse'] / other_planet['pl_bmasse']), 3)
                else:
                    mass_ratio = round((other_planet['pl_bmasse'] / planet['pl_bmasse']), 3)

                # Check if the mass ratio is below the threshold
                sign_check = np.sign(planet['vx'])==np.sign(other_planet['vx']) and np.sign(planet['vy'])==np.sign(other_planet['vy']) and np.sign(planet['vz'])==np.sign(other_planet['vz'])
                v_norm=np.linalg.norm([planet['vx'],planet['vy'],planet['vz']]);
                distance=np.linalg.norm([planet['x']-other_planet['x'],planet['y']-other_planet['y'],planet['z']-other_planet['z']]);
                f_gravitation=39.4784*planet['pl_bmasse']*other_planet['pl_bmasse']/pow(distance,2)
                f_centripetal=(1/distance)*planet['pl_bmasse']*v_norm*v_norm
                force_check=f_gravitation>f_centripetal
                if mass_ratio < threshold_mass_ratio and sign_check and force_check:
                    # Initialize the list if not already present
                    if planet['pl_name'] not in store_max_mass_ratio:
                        # print(mass_ratio)
                        store_max_mass_ratio[planet['pl_name']] = []
                    store_max_mass_ratio[planet['pl_name']].append(other_planet['pl_name'])
    # data['planetary'] = [None] * len(data)
    # for i,name in enumerate(data['pl_name']):
    #     data['planetary'][i]=store_max_mass_ratio.get(name, [])
    #     # else:
    #       pip  # data['planetary'][i]=[]
    #     print(type(data['planetary'][i]))


    # data['planetary'] = [store_max_mass_ratio.get(name, []) for name in data['pl_name']]
    '''
    for idx, vals in data['planetary'].items():
        data['planetary'][idx] = list(vals)
        # data.iloc[idx, 'planetary'] = list(vals)
        # if type(vals) != list:
        #     data.iloc[idx, 'planetary'] = vals.to_list()
    '''
    return data, store_max_mass_ratio


# def calculate_important_parameters(data: pd.DataFrame) -> pd.DataFrame:  # type: ignore
#     """
#     Calculate important parameters for the dataset.

#     Args:
#         data (pd.DataFrame): Input DataFrame.

#     Returns:
#         pd.DataFrame: DataFrame with important parameters.
#     """
#     # Required columns for calculations
#     required_columns = ['pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 'pl_orblper', 'pl_Omega', 'pl_orbper']

#     # Validate required columns exist in the DataFrame
#     for col in required_columns:
#         if col not in data.columns:
#             raise ValueError(f"Missing required column: {col}")

#     # Compute orbital parameters
#     for idx, planet in data.iterrows():
#         if not all(pd.notnull(planet[col]) for col in required_columns):
#             continue
        
#         t = np.linspace(0, 2 * np.pi, 100)  # Full orbit in radians, with 100 points
#         # Pre-compute the full orbital path
#         vx_orbit, vy_orbit, vz_orbit = compute_orbit_velocity(
#             a=planet['pl_orbsmax'],
#             e=planet['pl_orbeccen'],
#             i=np.radians(planet['pl_orbincl']),
#             omega=np.radians(planet['pl_orblper']),
#             Omega=np.radians(planet['pl_Omega']),
#             t=t
#         )

#         x_orbit, y_orbit, z_orbit = compute_orbit_path(
#             a=planet['pl_orbsmax'],
#             e=planet['pl_orbeccen'],
#             i=np.radians(planet['pl_orbincl']),
#             omega=np.radians(planet['pl_orblper']),
#             Omega=np.radians(planet['pl_Omega']),
#             t=t
#         )
        
#         # Assign initial position and velocity to the DataFrame
#         data.loc[idx, ['vx', 'vy', 'vz']] = round(vx_orbit[0], 5), round(vy_orbit[0], 5), round(vz_orbit[0], 5)
#         data.loc[idx, ['x', 'y', 'z']] = round(x_orbit[0], 5), round(y_orbit[0], 5), round(z_orbit[0], 5)

#     # Mass ratio and force calculations
#     threshold_mass_ratio = 0.01
#     store_max_mass_ratio = {}

#     for i, planet in data.iterrows():
#         for j, other_planet in data.iterrows():
#             if planet['pl_name'] == other_planet['pl_name']:
#                 continue
#             if planet['pl_bmasse'] > 0 and other_planet['pl_bmasse'] > 0:
#                 mass_ratio = round(min(planet['pl_bmasse'], other_planet['pl_bmasse']) /
#                                    max(planet['pl_bmasse'], other_planet['pl_bmasse']), 3)
                
#                 distance = np.linalg.norm([planet['x'] - other_planet['x'], 
#                                            planet['y'] - other_planet['y'], 
#                                            planet['z'] - other_planet['z']])
#                 if distance == 0:
#                     continue

#                 v_norm = np.linalg.norm([planet['vx'], planet['vy'], planet['vz']])
#                 f_gravitation = 39.4784 * planet['pl_bmasse'] * other_planet['pl_bmasse'] / (distance ** 2)
#                 f_centripetal = (1 / distance) * planet['pl_bmasse'] * (v_norm ** 2)

#                 sign_check = all(np.sign(planet[col]) == np.sign(other_planet[col]) for col in ['vx', 'vy', 'vz'])
#                 force_check = f_gravitation > f_centripetal

#                 if mass_ratio < threshold_mass_ratio and sign_check and force_check:
#                     store_max_mass_ratio.setdefault(planet['pl_name'], []).append(other_planet['pl_name'])

#     # Assign results to the 'planetary' column
#     data['planetary'] = [store_max_mass_ratio.get(name, []) for name in data['pl_name']]

#     return data, store_max_mass_ratio



def compute_orbit_path(a: float, e: float, i: float, omega: float, Omega: float, t: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray): # type: ignore
    """
    Compute the full elliptical orbit in 3D space.
    
    Args:
        a: Semi-major axis in AU.
        e: Orbital eccentricity.
        i: Orbital inclination in radians.
        omega: Argument of periapsis in radians.
        Omega: Longitude of ascending node in radians.
    
    Returns:
        x, y, z: Arrays representing the orbital path in 3D space.
    """
    # True anomaly (v) over one complete orbit
    # v = np.linspace(0, 2 * np.pi, 1)
    v = t
    
    # Orbital radius (r) as a function of v
    r = (a * (1 - e**2)) / (1 + e * np.cos(v))
    
    # Orbital positions in the orbital plane
    x_orbit = r * np.cos(v)
    y_orbit = r * np.sin(v)
    z_orbit = np.zeros_like(x_orbit)
    
    # Rotation matrices
    Rz_Omega = np.array([[np.cos(Omega), -np.sin(Omega), 0],
                         [np.sin(Omega),  np.cos(Omega), 0],
                         [0,              0,             1]])
    
    Rx_i = np.array([[1, 0,            0],
                     [0, np.cos(i), -np.sin(i)],
                     [0, np.sin(i),  np.cos(i)]])
    
    Rz_omega = np.array([[np.cos(omega), -np.sin(omega), 0],
                         [np.sin(omega),  np.cos(omega), 0],
                         [0,              0,             1]])
    
    # Full rotation matrix
    rotation_matrix = Rz_Omega @ Rx_i @ Rz_omega
    
    # Rotate the orbit into 3D space
    orbit = np.array([x_orbit, y_orbit, z_orbit])
    x, y, z = rotation_matrix @ orbit
    # print(x, y, z)
    
    return x, y, z


def compute_orbit_velocity(a: float, e: float, i: float, omega: float, Omega: float, t: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):   # type: ignore
    """
    Compute the velocity components (vx, vy, vz) along the elliptical orbit in 3D space.
    
    Args:
        a: Semi-major axis in AU.
        e: Orbital eccentricity.
        i: Orbital inclination in radians.
        omega: Argument of periapsis in radians.
        Omega: Longitude of ascending node in radians.
    
    Returns:
        vx, vy, vz: Arrays representing velocity components in 3D space.
    """
    # True anomaly (v) over one complete orbit
    # v = np.linspace(0, 2 * np.pi, 1)
    v = t
    
    # Orbital radius (r) as a function of v
    r = (a * (1 - e**2)) / (1 + e * np.cos(v))
    
    # Orbital speed in the orbital plane (vis-viva equation)
    mu = 4 * np.pi**2  # Gravitational parameter in AU^3/year^2 for solar mass
    orbital_speed = np.sqrt(mu * (2 / r - 1 / a))  # Speed in AU/year
    
    # Orbital positions in the orbital plane
    x_orbit = r * np.cos(v)
    y_orbit = r * np.sin(v)
    z_orbit = np.zeros_like(x_orbit)
    
    # Velocity in the orbital plane
    vx_orbit = -orbital_speed * np.sin(v)
    vy_orbit = orbital_speed * np.cos(v)
    vz_orbit = np.zeros_like(vx_orbit)
    
    # Rotation matrices
    Rz_Omega = np.array([[np.cos(Omega), -np.sin(Omega), 0],
                         [np.sin(Omega),  np.cos(Omega), 0],
                         [0,              0,             1]])
    
    Rx_i = np.array([[1, 0,            0],
                     [0, np.cos(i), -np.sin(i)],
                     [0, np.sin(i),  np.cos(i)]])
    
    Rz_omega = np.array([[np.cos(omega), -np.sin(omega), 0],
                         [np.sin(omega),  np.cos(omega), 0],
                         [0,              0,             1]])
    
    # Full rotation matrix
    rotation_matrix = Rz_Omega @ Rx_i @ Rz_omega
    
    # Rotate the velocity into 3D space
    velocity_orbit = np.array([vx_orbit, vy_orbit, vz_orbit])
    vx, vy, vz = rotation_matrix @ velocity_orbit
    
    return vx, vy, vz


import numpy as np

# Orbital parameters (example values)
a = 1.0  # Semi-major axis in AU
e = 0.1  # Eccentricity
i = np.radians(30)  # Inclination in radians
omega = np.radians(50)  # Argument of periapsis in radians
Omega = np.radians(100)  # Longitude of ascending node in radians

# Orbital period (T)
mu = 4 * np.pi**2  # Gravitational parameter for the Sun in AU^3/year^2
T = 2 * np.pi * np.sqrt(a**3 / mu)  # Orbital period in years

# Initial time (t0) and position (x0, y0, z0)
t0 = 0  # Initial time (in years)
x0, y0, z0 = 1.0, 0.0, 0.0  # Initial position in AU (on the x-axis)

# Initial velocity (vx0, vy0, vz0)
vx0, vy0, vz0 = 0.0, np.sqrt(mu / a), 0.0  # Example initial velocity for circular orbit

# Time step for the simulation (in years)
delta_t = 0.1  # Time step (e.g., 0.1 years)

# Function to calculate mean anomaly
def mean_anomaly(t, T):
    return (2 * np.pi / T) * t

# Solve Kepler's equation to get eccentric anomaly
def eccentric_anomaly(M, e):
    E = M
    for _ in range(10):  # Iterative method for solving Kepler's equation
        E = M + e * np.sin(E)
    return E

# Function to calculate true anomaly from eccentric anomaly
def true_anomaly(E, e):
    return 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))


# Simulate the orbit by moving forward in time
def simulate_orbit(t0, x0, y0, z0, vx0, vy0, vz0, delta_t, T, a, e, i, omega, Omega):
    # Calculate the mean anomaly at the next time step
    t1 = t0 + delta_t  # New time step
    M1 = mean_anomaly(t1, T)  # Mean anomaly for the next time step
    
    # Solve Kepler's equation to find the eccentric anomaly
    E1 = eccentric_anomaly(M1, e)
    
    # Find the true anomaly for the next time step
    v1 = true_anomaly(E1, e)
    
    # Calculate the orbital radius (r) and speed at the next position
    r1 = (a * (1 - e**2)) / (1 + e * np.cos(v1))
    orbital_speed = np.sqrt(mu * (2 / r1 - 1 / a))  # Orbital speed
    
    # Compute the position and velocity in the orbital plane
    x_orbit1 = r1 * np.cos(v1)
    y_orbit1 = r1 * np.sin(v1)
    z_orbit1 = 0  # Assuming the orbit lies in the equatorial plane
    
    vx_orbit1 = -orbital_speed * np.sin(v1)
    vy_orbit1 = orbital_speed * np.cos(v1)
    vz_orbit1 = 0  # Assuming the orbital velocity lies in the equatorial plane
    
    # Rotation matrices for 3D space
    Rz_Omega = np.array([[np.cos(Omega), -np.sin(Omega), 0],
                         [np.sin(Omega), np.cos(Omega), 0],
                         [0, 0, 1]])
    
    Rx_i = np.array([[1, 0, 0],
                     [0, np.cos(i), -np.sin(i)],
                     [0, np.sin(i), np.cos(i)]])
    
    Rz_omega = np.array([[np.cos(omega), -np.sin(omega), 0],
                         [np.sin(omega), np.cos(omega), 0],
                         [0, 0, 1]])
    
    # Full rotation matrix
    rotation_matrix = Rz_Omega @ Rx_i @ Rz_omega
    
    # Rotate the position and velocity vectors into 3D space
    position = np.array([x_orbit1, y_orbit1, z_orbit1])
    velocity = np.array([vx_orbit1, vy_orbit1, vz_orbit1])
    
    x1, y1, z1 = rotation_matrix @ position
    vx1, vy1, vz1 = rotation_matrix @ velocity
    
    return x1, y1, z1, vx1, vy1, vz1



def calculate_orbital_parameters(data):
    """
    Calculate orbital parameters ('a', 'e', 'i_deg', 'Omega_deg', 'omega_deg', 'nu_deg') 
    for each planet in the dataframe.

    Args:
        data (pd.DataFrame): DataFrame with columns ['x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'mass', 
                                                   'centroid_x', 'centroid_y', 'centroid_z', 'centroid_mass'].

    Returns:
        pd.DataFrame: DataFrame with added columns ['a', 'e', 'i_deg', 'Omega_deg', 'omega_deg', 'nu_deg'].
    """
    G = 6.67430e-11  # Gravitational constant

    # Initialize columns
    data['a'] = 0
    data['e'] = 0
    data['i_deg'] = 0
    data['Omega_deg'] = 0
    data['omega_deg'] = 0
    data['nu_deg'] = 0

    for idx, row in data.iterrows():
        # Extract relative position and velocity
        rx, ry, rz = row['x'] - row['centroid_x'], row['y'] - row['centroid_y'], row['z'] - row['centroid_z']
        vx, vy, vz = row['vx'], row['vy'], row['vz']
        r = np.sqrt(rx**2 + ry**2 + rz**2)
        v = np.sqrt(vx**2 + vy**2 + vz**2)

        # Gravitational parameter (mu)
        mu = G * (row['mass'] + row['centroid_mass'])

        # Specific orbital energy
        energy = (v**2) / 2 - mu / r

        # Semi-major axis (a)
        a = -mu / (2 * energy)

        # Angular momentum vector
        h = np.cross([rx, ry, rz], [vx, vy, vz])
        h_mag = np.linalg.norm(h)

        # Eccentricity vector
        e_vec = (np.cross([vx, vy, vz], h) / mu) - np.array([rx, ry, rz]) / r
        e = np.linalg.norm(e_vec)

        # Inclination (i)
        i = np.arccos(h[2] / h_mag)

        # Node vector
        n = np.cross([0, 0, 1], h)
        n_mag = np.linalg.norm(n)

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

        # Assign values
        data.at[idx, 'a'] = a
        data.at[idx, 'e'] = e
        data.at[idx, 'i_deg'] = np.degrees(i)
        data.at[idx, 'Omega_deg'] = np.degrees(Omega)
        data.at[idx, 'omega_deg'] = np.degrees(omega)
        data.at[idx, 'nu_deg'] = np.degrees(nu)

    return data

'''
import numpy as np
import pandas as pd

def calculate_orbital_parameters(data):
    """
    Calculate orbital parameters ('a', 'e', 'i_deg', 'Omega_deg', 'omega_deg', 'nu_deg') 
    for each planet in the dataframe.

    Args:
        data (pd.DataFrame): DataFrame with columns ['x', 'y', 'z', 'vx', 'vy', 'vz', 'mass', 
                                                     'centroid_x', 'centroid_y', 'centroid_z', 'centroid_mass'].

    Returns:
        pd.DataFrame: DataFrame with added columns ['a', 'e', 'i_deg', 'Omega_deg', 'omega_deg', 'nu_deg'].
    """
    G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)

    # Initialize columns for orbital parameters
    data['a'] = 0.0
    data['e'] = 0.0
    data['i_deg'] = 0.0
    data['Omega_deg'] = 0.0
    data['omega_deg'] = 0.0
    data['nu_deg'] = 0.0

    for idx, row in data.iterrows():
        # Extract relative position and velocity vectors
        r_vec = np.array([row['x'] - row['centroid_x'], row['y'] - row['centroid_y'], row['z'] - row['centroid_z']])
        v_vec = np.array([row['vx'], row['vy'], row['vz']])
        r = np.linalg.norm(r_vec)  # Magnitude of position vector
        v = np.linalg.norm(v_vec)  # Magnitude of velocity vector

        # Gravitational parameter (mu)
        mu = G * (row['mass'] + row['centroid_mass'])

        # Specific orbital energy
        energy = (v**2) / 2 - mu / r

        # Semi-major axis (a)
        if energy != 0:
            a = -mu / (2 * energy)
        else:
            a = np.inf  # Parabolic or escape trajectory

        # Angular momentum vector and magnitude
        h_vec = np.cross(r_vec, v_vec)
        h_mag = np.linalg.norm(h_vec)

        # Eccentricity vector and magnitude
        e_vec = (np.cross(v_vec, h_vec) / mu) - (r_vec / r)
        e = np.linalg.norm(e_vec)

        # Inclination (i)
        i = np.arccos(np.clip(h_vec[2] / h_mag, -1, 1))  # Clip to avoid floating-point issues

        # Node vector and magnitude
        n_vec = np.cross([0, 0, 1], h_vec)
        n_mag = np.linalg.norm(n_vec)

        # Longitude of ascending node (Omega)
        Omega = 0.0
        if n_mag != 0:
            Omega = np.arccos(np.clip(n_vec[0] / n_mag, -1, 1))
            if n_vec[1] < 0:
                Omega = 2 * np.pi - Omega

        # Argument of periapsis (omega)
        omega = 0.0
        if n_mag != 0 and e != 0:
            omega = np.arccos(np.clip(np.dot(n_vec, e_vec) / (n_mag * e), -1, 1))
            if e_vec[2] < 0:
                omega = 2 * np.pi - omega

        # True anomaly (nu)
        nu = 0.0
        if e != 0:
            nu = np.arccos(np.clip(np.dot(e_vec, r_vec) / (e * r), -1, 1))
            if np.dot(r_vec, v_vec) < 0:
                nu = 2 * np.pi - nu

        # Assign results
        data.at[idx, 'a'] = a
        data.at[idx, 'e'] = e
        data.at[idx, 'i_deg'] = np.degrees(i)
        data.at[idx, 'Omega_deg'] = np.degrees(Omega)
        data.at[idx, 'omega_deg'] = np.degrees(omega)
        data.at[idx, 'nu_deg'] = np.degrees(nu)

    return data
'''