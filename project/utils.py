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
    E = mean_anomaly  # Initial guess for Eccentric Anomaly
    iteration = 0

    while iteration < max_iterations:
        delta_E = (E - eccentricity * np.sin(E) - mean_anomaly) / (1 - eccentricity * np.cos(E))
        E -= delta_E
        
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
    true_anomaly = 2 * np.arctan2(
        np.sqrt(1 + eccentricity) * np.sin(E / 2),
        np.sqrt(1 - eccentricity) * np.cos(E / 2)
    )
    
    return true_anomaly

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
