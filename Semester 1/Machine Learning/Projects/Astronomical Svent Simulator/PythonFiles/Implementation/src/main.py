# load save joblib model
import joblib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from utils import simulate_orbit
from GalaxyPredict import feature_engineering 



def load_model():
    model = joblib.load('../../save_models/rfr_model.joblib')
    return model


def predict(model, data):
    data = feature_engineering(data)
    # Make predictions using the loaded model
    predictions = model.predict(data)
    return predictions


def plot_results(predictions, data):
    x0 = data['x']; y0 = data['y']; z0 = data['z']
    vx0 = data['vx']; vy0 = data['vy']; vz0 = data['vz']
    a = predictions['a']; e = predictions['e']; i = predictions['i']; omega = predictions['omega']; Omega = predictions['Omega'];
    # Orbital period (T)
    mu = 4 * np.pi**2  # Gravitational parameter for the Sun in AU^3/year^2
    T = 2 * np.pi * np.sqrt(a**3 / mu)  # Orbital period in years
    
    # Simulate the orbit
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for i in range(100):
        x, y, z, vx, vy, vz = simulate_orbit(x0, y0, z0, vx0, vy0, vz0, T, a, e, i, omega, Omega)
        ax.plot3D(x0, y0, z0)
        x0 = x; y0 = y; z0 = z; vx0 = vx; vy0 = vy; vz0 = vz
        plt.show()
    

if __name__ == "__main__":
    model = load_model()
    # mass,x,y,z,vx,vy,vz,Cluster,centroid_mass,centroid_x,centroid_y,centroid_z
    # 1.503506623504771e+27,256212.73190432,142618.58168387,619428.7889181,-3.14073536e-24,-1.74826293e-24,-7.59315075e-24,0,1.4858392599900622e+28,379288.01092443,362643.94729617,741690.10197571
    dts = {
        'mass': [1.503506623504771e+27],
        'x': [256212.73190432],
        'y': [142618.58168387],
        'z': [619428.7889181],
        'vx': [-3.14073536e-24],
        'vy': [-1.74826293e-24],
        'vz': [-7.59315075e-24],
        'centroid_mass': [1.4858392599900622e+28],
        'centroid_x': [379288.01092443],
        'centroid_y': [362643.94729617],
        'centroid_z': [741690.10197571]
    }
    data = pd.DataFrame(dts)
    predict = predict(model, data)

    plot_results(predict, data)



