import pandas as pd


def main_version1():
    file_path = '../../astrCsv.csv'
    data = pd.read_csv(file_path, low_memory=False, index_col=0)
    # Mass of the planet, and Start
    # Eccentricity of the orbit
    # Semi-major axis of the orbit
    # Orbital period of the planet
    # Orbital inclination of the planet
    # Semi-minor axis of the orbit
    # Velocity and Radius


'''
    function:
    input palnets data:
            - initial velocity
            - initial position
            - Mass
    output:
            - Label: palnet name
'''
    

def main_version2():
    pass


if __name__ == "__main__":
    main_version1()
    # main_version2()