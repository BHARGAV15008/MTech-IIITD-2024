import numpy as np
from PythonFiles.Implementation.src.Preprocessing import handle_missing_values
from matplotlib import pyplot as plt
import seaborn as sns

def display_and_close(fig, delay=2):
    plt.pause(delay)
    plt.close(fig)

def univariant_analysis(data):
    data = handle_missing_values(data)

    fig = plt.figure(figsize=(10, 6))
    sns.histplot(data['pl_orbper'], bins=50, kde=True, color='blue')
    plt.title("Distribution of Orbital Periods")
    plt.xlabel("Orbital Period [days]")
    plt.ylabel("Frequency")
    display_and_close(fig)

    fig = plt.figure(figsize=(10, 6))
    sns.countplot(y=data['discoverymethod'], order=data['discoverymethod'].value_counts().index)
    plt.title("Discovery Methods Count")
    display_and_close(fig)

def bivariant_analysis(data):
    data = handle_missing_values(data)

    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(x='pl_orbper', y='pl_rade', data=data, hue='discoverymethod', alpha=0.7)
    plt.title("Orbital Period vs Radius")
    plt.xlabel("Orbital Period [days]")
    plt.ylabel("Radius [Earth Radii]")
    display_and_close(fig)

    fig = plt.figure(figsize=(8, 6))
    sns.scatterplot(x='pl_rade', y='pl_bmasse', data=data, hue='discoverymethod', alpha=0.7)
    plt.title("Planet Radius vs Mass (Colored by Discovery Method)")
    plt.xlabel("Planet Radius [Earth Radii]")
    plt.ylabel("Planet Mass [Earth Mass]")
    plt.legend(loc='best')
    display_and_close(fig)

    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(x='pl_bmasse', y='pl_orbper', data=data, hue='discoverymethod', alpha=0.7)
    plt.title("Mass vs Orbital Period")
    plt.xlabel("Mass [Earth Mass]")
    plt.ylabel("Orbital Period [days]")
    display_and_close(fig)

def time_based_analysis(data):
    data = handle_missing_values(data)

    fig = plt.figure(figsize=(10, 6))
    sns.histplot(data['pl_orbper'], bins=50, kde=True, color='blue')
    plt.title("Distribution of Orbital Periods")
    plt.xlabel("Orbital Period [days]")
    plt.ylabel("Frequency")
    display_and_close(fig)

    fig = plt.figure(figsize=(12, 6))
    discovery_trends = data['disc_year'].value_counts().sort_index()
    sns.lineplot(x=discovery_trends.index, y=discovery_trends.values)
    plt.title("Number of Discoveries Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Discoveries")
    display_and_close(fig)

def spatial_analysis(data):
    data = handle_missing_values(data)

    fig = plt.figure(figsize=(10, 8))
    sns.scatterplot(x=data['ra'], y=data['dec'], alpha=0.5, color='purple')
    plt.title("Star Map (RA vs Dec)")
    plt.xlabel("RA [deg]")
    plt.ylabel("Dec [deg]")
    display_and_close(fig)

    fig = plt.figure(figsize=(10, 8))
    sns.scatterplot(x=data['glon'], y=data['glat'], alpha=0.5, color='green')
    plt.title("Galactic Coordinates (Longitude vs Latitude)")
    plt.xlabel("Galactic Longitude [deg]")
    plt.ylabel("Galactic Latitude [deg]")
    display_and_close(fig)