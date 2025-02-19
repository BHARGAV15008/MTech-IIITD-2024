import pandas as pd
import numpy as np
import re  # Regular expression library

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        """Load data from a CSV file."""
        return pd.read_csv(self.file_path, low_memory=False)

class DataPreprocessor:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def convert_rastr_to_degrees(self, rastr: str) -> float:
        """Convert Right Ascension in time format to decimal degrees."""
        if not isinstance(rastr, str):
            return np.nan

        time_parts = rastr.split('h')
        hours = float(time_parts[0])
        minutes, seconds = time_parts[1].split('m')
        minutes = float(minutes)
        seconds = float(seconds.replace('s', ''))

        return 15 * (hours + minutes / 60 + seconds / 3600)

    def handle_missing_values(self) -> pd.DataFrame:
        """Handle missing values in the DataFrame."""
        if 'rastr' in self.data.columns:
            self.data['ra_deg'] = self.data['rastr'].apply(self.convert_rastr_to_degrees)

        # Drop columns with > 50% missing values, keeping only the key columns
        key_columns = [
            'ra_deg', 'ra', 'dec', 'glon', 'glat', 'sy_pmdec', 
            'st_radv', 'sy_pmra', 'sy_plx', 'pl_orbper', 'pl_orbincl', 
            'pl_orblper', 'pl_orbeccen', 'pl_orbsmax'
        ]
        missing_threshold = 0.5
        columns_to_drop = self.data.columns[self.data.isnull().mean() > missing_threshold].difference(key_columns)
        self.data.drop(columns=columns_to_drop, inplace=True)

        # Fill numerical columns with median
        for col in self.data.select_dtypes(include=[np.number]).columns:
            self.data[col] = self.data[col].fillna(self.data[col].median())

        # Fill categorical columns with mode
        for col in self.data.select_dtypes(include=['object']).columns:
            self.data[col] = self.data[col].astype(str)  # Ensure uniform type
            self.data[col] = self.data[col].fillna(self.data[col].mode()[0])

        # Ensure numerical columns are properly cast
        numeric_columns = [
            'pl_orbsmax', 'pl_orbeccen', 'pl_orbincl', 
            'pl_orblper', 'pl_orbper'
        ]
        for col in numeric_columns:
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')

        return self.data

    def clean_html_and_convert_to_nan(self, text):
        """Clean HTML tags from text and convert to float or return NaN."""
        clean = re.compile("<.*?>")
        cleaned_text = re.sub(clean, "", str(text))

        try:
            return float(cleaned_text)
        except ValueError:
            return np.nan 

    def remove_html_tags(self) -> None:
        """Remove HTML tags from columns that likely contain HTML and convert to NaN."""
        # Check each column to see if it contains HTML-like content
        for column in self.data.select_dtypes(include=['object']).columns:
            if self.data[column].astype(str).str.contains('<').any():  # Check for presence of '<'
                self.data[column] = self.data[column].apply(self.clean_html_and_convert_to_nan)