import numpy as np
import pandas as pd
from utils import large_omega

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    return pd.read_csv(file_path, low_memory=False, index_col=0)

def remove_some_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Remove some columns from the DataFrame."""
    # substring = 'reflink'
    for col in data.columns:
        if 'reflink' in col or 'refname' in col:
            data.drop(col, axis=1, inplace=True)
    
    cols = ['pl_name',
            'hostname',
            'pl_letter',
            'hd_name',
            'hip_name',
            'tic_id',
            'gaia_id',
            'discoverymethod',
            'disc_locale',
            'disc_facility',
            'disc_instrument',
            'pl_bmassprov',
            'pl_orbtper_systemref',
            'pl_tranmid_systemref',
            'st_metratio',
            'disc_telescope',
            'disc_year',
            'disc_pubdate',
            'st_spectype']


    for col in cols:
        data.drop(col, axis=1, inplace=True)
    return data

def convert_rastr_to_degrees(rastr: str) -> float:
    """Convert Right Ascension in time format to decimal degrees."""
    if not isinstance(rastr, str):
        return np.nan

    time_parts = rastr.split('h')
    hours = float(time_parts[0])
    minutes, seconds = time_parts[1].split('m')
    minutes = float(minutes)
    seconds = float(seconds.replace('s', ''))

    return 15 * (hours + minutes / 60 + seconds / 3600)

def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values in a DataFrame."""
    data = large_omega(data)
    if 'rastr' in data.columns:
        data['ra_deg'] = data['rastr'].apply(convert_rastr_to_degrees)

    # Drop columns with > 50% missing values, keeping only the key columns
    key_columns = [
        'ra_deg', 'ra', 'dec', 'glon', 'glat', 'sy_pmdec', 
        'st_radv', 'sy_pmra', 'sy_plx', 'pl_orbper', 'pl_orbincl', 
        'pl_orblper', 'pl_orbeccen', 'pl_orbsmax'
    ]
    missing_threshold = 0.75
    columns_to_drop = data.columns[data.isnull().mean() > missing_threshold].difference(key_columns)
    data.drop(columns=columns_to_drop, inplace=True)

    # Fill numerical columns with median
    for col in data.select_dtypes(include=[np.number]).columns:
        data[col] = data[col].fillna(data[col].median())  # Replacing inplace=True with direct assignment

    # Fill categorical columns with mode, ensure uniform type before filling
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].astype(str)  # Ensure uniform type
        data[col] = data[col].fillna(data[col].mode()[0])  # Replacing inplace=True with direct assignment

    # Ensure numerical columns are properly cast
    data['pl_orbsmax'] = pd.to_numeric(data['pl_orbsmax'], errors='coerce')
    data['pl_orbeccen'] = pd.to_numeric(data['pl_orbeccen'], errors='coerce')
    data['pl_orbincl'] = pd.to_numeric(data['pl_orbincl'], errors='coerce')
    data['pl_orblper'] = pd.to_numeric(data['pl_orblper'], errors='coerce')
    data['pl_orbper'] = pd.to_numeric(data['pl_orbper'], errors='coerce')

    return data
