from sklearn.datasets import make_regression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR, LinearSVR
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.impute import SimpleImputer

def outliers(data, threshold=0.5):
    print(f"old data.shape:{data.shape}")
    q_low=data['pl_bmasse'].quantile(0.01)
    q_high=data['pl_bmasse'].quantile(0.99)
    upper_index=data.index[data['pl_bmasse']>(q_high+threshold*(q_high-q_low))].tolist()
    lower_index=data.index[data['pl_bmasse']>(q_low-threshold*(q_high-q_low))].tolist()
    print(f"upper_index length:{len(upper_index)}")
    print(f"lower_index length:{len(lower_index)}")

    df=data.drop(upper_index+lower_index)
    print(f"new data.shape:{df.shape}")
    return df

# Load data
df = pd.read_excel('updated_training_data.xlsx')
print(f"\t -->  df.columns:{df.columns}")
# df=outliers(data=df,threshold=1.5)
low_mass_row_index=df.index[df['pl_bmasse']<10].to_list()
df.drop(low_mass_row_index,inplace=True)

X = df[['x', 'y', 'z', 'vx', 'vy', 'vz', 'pl_bmasse', 'pl_Omega']]
# X = df[['x', 'y', 'z', 'vx', 'vy', 'vz', 'pl_bmasse', 'pl_Omega', 'pl_orbsmax', 'pl_orbper', 'pl_orbincl']]
# X = df[['x', 'y', 'z', 'vx', 'vy', 'vz', 'pl_bmasse', 'pl_Omega', 'pl_orbsmax', 'pl_orbper', 'pl_orbeccen']]
# X = df[['x', 'y', 'z', 'vx', 'vy', 'vz', 'pl_bmasse', 'pl_Omega', 'pl_orbper', 'pl_orbsmax']]
y = df[['pl_orbincl', 'pl_orbsmax', 'pl_orbeccen', 'pl_orblper', 'pl_orbper']]
# y = df[['pl_orbincl', 'pl_orbeccen', 'pl_orblper']]
# y = df[['pl_orbeccen', 'pl_orblper']]
# y = df[['pl_orbincl', 'pl_orblper']]
# y = df[['pl_orbeccen', 'pl_orblper']]


def version_one():
    X['vx2'] = X['vx'] * X['vx']
    X['vy2'] = X['vy'] * X['vy']
    X['vz2'] = X['vz'] * X['vz']
    X['v']=np.sqrt(X['vx2']+X['vy2']+X['vz2'])
    X['vxvy'] = X['vx'] * X['vy']
    X['vxvz'] = X['vx'] * X['vz']
    X['vyvz'] = X['vy'] * X['vz']
    # X['vxvyvz'] = X['vx'] * X['vy'] + X['vy'] * X['vz'] + X['vz'] * X['vx']
    # X['vxvyvz2'] = X['vx'] * X['vx'] + X['vy'] * X['vy'] + X['vz'] * X['vz']
    # X['vx_plus_vy'] = X['vx'] * X['vx'] + X['vy'] * X['vy']
    # X['vx_plus_vz'] = X['vx'] * X['vx'] + X['vz'] * X['vz']
    # X['vy_plus_vz'] = X['vy'] * X['vy'] + X['vz'] * X['vz']
    # X['vx_minus_vy'] = X['vx'] * X['vx'] - X['vy'] * X['vy']
    # X['vx_minus_vz'] = X['vx'] * X['vx'] - X['vz'] * X['vz']
    # X['vy_minus_vz'] = X['vy'] * X['vy'] - X['vz'] * X['vz']
    # X['pl_bmasse_sqrt'] = np.sqrt(X['pl_bmasse']) * np.pow(X['pl_bmasse'], 2)
    X['pl_bmasse_sqrt'] = np.sqrt(X['pl_bmasse'])
    X['x2'] = X['x'] * X['x']
    X['y2'] = X['y'] * X['y']
    X['z2'] = X['z'] * X['z']
    X['r'] = np.sqrt(X['x2'] + X['y2'] + X['z2'])
    X['r2'] = X['x2'] + X['y2'] + X['z2']
    X['r2O'] = X['r'] * X['r'] * X['pl_Omega'] 
    X['pl_bmasse']=4.3009e-6*X['pl_bmasse'] # Gravitational constant times mass of the planet
    h = np.cross(X[['x', 'y', 'z']].to_numpy(), X[['vx', 'vy', 'vz']].to_numpy())
    h_mag = np.linalg.norm(h, axis=1)
    h_z = h[:,2]
    # print(f"shape of h_z:{h_z.shape}")
    # print(f"shape of h_mag:{h_mag.shape}")
    X['h_z'] = h_z
    X['h_mag'] = h_mag
    # =====================================================================
    mu = 398600  # km^3/s^2
    '''
    # # Position and velocity vectors
    r = X[['x', 'y', 'z']].to_numpy()
    v = X[['vx', 'vy', 'vz']].to_numpy()

    # # Angular momentum vector and its magnitude
    h = np.cross(r, v)
    h_mag = np.linalg.norm(h, axis=1)
    h_z = h[:, 2]

    # # Eccentricity vector
    r_mag = np.linalg.norm(r, axis=1).reshape(-1, 1)
    v_mag = np.linalg.norm(v, axis=1).reshape(-1, 1)
    e_vector = (np.cross(v, h) / mu) - (r / r_mag)
    e_mag = np.linalg.norm(e_vector, axis=1)

    # # Node vector
    k = np.array([0, 0, 1])  # Unit vector normal to reference plane
    n_vector = np.cross(k, h)
    n_mag = np.linalg.norm(n_vector, axis=1)

    # # Dot product between node vector and eccentricity vector
    n_dot_e = np.sum(n_vector * e_vector, axis=1)
    X['hy_by_hx'] = np.arctan(h[:, 1] / h[:, 0])
    X['ey_by_ex'] = np.arctan(e_vector[:, 1] / e_vector[:, 0])
    X['h_minus_e'] = X['ey_by_ex'] - X['hy_by_hx']
    # # # Add these features to the DataFrame
    X['h_z'] = h_z
    X['h_y'] = h[:, 1]
    X['h_x'] = h[:, 0]
    # X['h_mag'] = h_mag
    # X['r_mag'] = r_mag.flatten()
    # X['v_mag'] = v_mag.flatten()
    X['e_x'], X['e_y'], X['e_z'] = e_vector[:, 0], e_vector[:, 1], e_vector[:, 2]
    # X['e_mag'] = e_mag
    # X['n_x'], X['n_y'] = n_vector[:, 0], n_vector[:, 1]
    # X['n_mag'] = n_mag
    # X['n_dot_e'] = n_dot_e

# ================================================

    # X['pl_bmasse_sqrt'] = np.sqrt(X['pl_bmasse']) / (X['vx']**2 + X['vy']**2 + X['vz']**2)
    # X['x2_plus_y2'] = X['x'] * X['x'] + X['y'] * X['y']
    # X['y2_plus_z2'] = X['y'] * X['y'] + X['z'] * X['z']
    # X['z2_plus_x2'] = X['z'] * X['z'] + X['x'] * X['x']
    # X['x2_plus_y2_plus_z2'] = X['x'] * X['x'] + X['y'] * X['y'] + X['z'] * X['z']
    # X['x2_minus_y2'] = X['x'] * X['x'] - X['y'] * X['y']
    # X['y2_minus_z2'] = X['y'] * X['y'] - X['z'] * X['z']
    # X['z2_minus_x2'] = X['z'] * X['z'] - X['x'] * X['x']
    # X['x2_minus_y2_minus_z2'] = X['x'] * X['x'] - X['y'] * X['y'] - X['z'] * X['z']
    # X['x2_minus_y2_plus_z2'] = X['x'] * X['x'] - X['y'] * X['y'] + X['z'] * X['z']
    # X['x2_plus_y2_minus_z2'] = X['x'] * X['x'] + X['y'] * X['y'] - X['z'] * X['z']
    '''

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=33)
    print(f"\t -->  X_train.shape:{X_train.shape}")
    print(f"\t -->  y_train.shape:{y_train.shape}")
    print(f"\t -->  X_test.shape:{X_test.shape}")
    print(f"\t -->  y_test.shape:{y_test.shape}")
    print()

    # #column 5 is the target variable
    # svr = SVR(C=2.0, epsilon=0.2, )
    # mor = mor.fit(X_train, y_train)

    # Create the SVR regressor
    # svr = LinearSVR(C=2.0, epsilon=0.2, )
    svr = SVR(C=1.0, epsilon=0.2,)
    # Create the Multioutput Regressor
    mor = MultiOutputRegressor(svr)

    # Train the regressor
    mor = mor.fit(X_train, y_train)

    # Generate predictions for testing data
    y_pred = mor.predict(X_test)

    # Convert y_test to NumPy array for slicing
    y_test_array = y_test.to_numpy()

    # Evaluate the regressor
    mse_one = mean_squared_error(y_test_array[:, 0], y_pred[:, 0])
    mse_two = mean_squared_error(y_test_array[:, 1], y_pred[:, 1])
    print(f'MSE for first regressor: {mse_one} - second regressor: {mse_two}')
    mae_one = mean_absolute_error(y_test_array[:, 0], y_pred[:, 0])
    mae_two = mean_absolute_error(y_test_array[:, 1], y_pred[:, 1])
    print(f'MAE for first regressor: {mae_one} - second regressor: {mae_two}')

    # FInding r2Score
    # r2_score_one = r2_score(y_test_array[:, 0], y_pred[:, 0])
    # r2_score_two = r2_score(y_test_array[:, 1], y_pred[:, 1])
    # print(f'r2Score for first regressor: {r2_score_one} - second regressor: {r2_score_two}')

    # print("y_test_array:", y_test_array[0])
    # print("y_pred:", y_pred[0])
    # # Evaluate
    # mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
    # r2 = r2_score(y_test, y_pred, multioutput='uniform_average')

    # print("SVR MSE:", mse)
    # print("SVR R²:", round(r2*100, 4),"%")
    # # Evaluate individual R² scores for each output variable
    # individual_r2_scores = r2_score(y_test, y_pred, multioutput='raw_values')
    # for i, r2 in enumerate(individual_r2_scores):
    #     print(f"R² for target {y.columns[i]}: {round(r2 * 100, 4)}%")



    # # Feature Scaling
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    # # Gradient Boosting Regressor
    # gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)
    # mor_gbr = MultiOutputRegressor(gbr)
    # mor_gbr.fit(X_train, y_train)

    # # Predictions
    # y_pred_gbr = mor_gbr.predict(X_test)

    # # Evaluate
    # mse = mean_squared_error(y_test, y_pred_gbr, multioutput='uniform_average')
    # r2 = r2_score(y_test, y_pred_gbr, multioutput='uniform_average')

    # print("Gradient Boosting MSE:", mse)
    # print("Gradient Boosting R²:", round(r2*100, 4),"%")
    # # Evaluate individual R² scores for each output variable
    # individual_r2_scores = r2_score(y_test, y_pred_gbr, multioutput='raw_values')
    # for i, r2 in enumerate(individual_r2_scores):
    #     print(f"R² for target {y.columns[i]}: {round(r2 * 100, 4)}%")

def version_two():
    # Feature Engineering
    X['vx2'] = X['vx'] * X['vx']
    X['vy2'] = X['vy'] * X['vy']
    X['vz2'] = X['vz'] * X['vz']
    X['vxvyvz'] = X['vx'] * X['vy'] + X['vy'] * X['vz'] + X['vz'] * X['vx']
    X['pl_bmasse_sqrt'] = np.sqrt(X['pl_bmasse'])
    X['x2_plus_y2'] = X['x'] * X['x'] + X['y'] * X['y']
    X['y2_plus_z2'] = X['y'] * X['y'] + X['z'] * X['z']
    X['x2_plus_y2_plus_z2'] = X['x'] * X['x'] + X['y'] * X['y'] + X['z'] * X['z']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=33)
    print(f"\t -->  X_train.shape:{X_train.shape}")
    print(f"\t -->  y_train.shape:{y_train.shape}")
    print(f"\t -->  X_test.shape:{X_test.shape}")
    print(f"\t -->  y_test.shape:{y_test.shape}")

    # Feature scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # -----------------------------------------------
    # 1. Gradient Boosting Regressor with Hyperparameter Tuning
    # -----------------------------------------------
    gbr = GradientBoostingRegressor()
    param_grid_gbr = {
        "n_estimators": [100, 200],
        "learning_rate": [0.05, 0.1, 0.2],
        "max_depth": [3, 5, 7],
    }

    grid_search_gbr = GridSearchCV(gbr, param_grid_gbr, scoring='r2', cv=3, verbose=1)
    mor_gbr = MultiOutputRegressor(grid_search_gbr)
    mor_gbr.fit(X_train, y_train)

    # Predictions
    y_pred_gbr = mor_gbr.predict(X_test)

    # Evaluate
    print("\nGradient Boosting Regressor Results:")
    print("Best Parameters:", mor_gbr.estimators_[0].best_params_)
    print("MSE:", mean_squared_error(y_test, y_pred_gbr, multioutput='uniform_average'))
    print("R²:", round(r2_score(y_test, y_pred_gbr, multioutput='uniform_average') * 100, 4), "%")

    # -----------------------------------------------
    # 2. Kernelized SVR with Hyperparameter Tuning
    # -----------------------------------------------
    svr = SVR()
    param_grid_svr = {
        "kernel": ["rbf", "poly"],
        "C": [0.1, 1, 10],
        "epsilon": [0.01, 0.1, 0.5],
    }

    grid_search_svr = GridSearchCV(svr, param_grid_svr, scoring='r2', cv=3, verbose=1)
    mor_svr = MultiOutputRegressor(grid_search_svr)
    mor_svr.fit(X_train, y_train)

    # Predictions
    y_pred_svr = mor_svr.predict(X_test)

    # Evaluate
    print("\nKernelized SVR Results:")
    print("Best Parameters:", mor_svr.estimators_[0].best_params_)
    print("MSE:", mean_squared_error(y_test, y_pred_svr, multioutput='uniform_average'))
    print("R²:", round(r2_score(y_test, y_pred_svr, multioutput='uniform_average') * 100, 4), "%")

    # -----------------------------------------------
    # 3. Ensemble SVR + Gradient Boosting + Random Forest
    # -----------------------------------------------
    rf = RandomForestRegressor(n_estimators=100, random_state=33)
    ensemble_model = VotingRegressor(estimators=[
        ('gbr', GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5)),
        ('svr', SVR(kernel='rbf', C=1, epsilon=0.1)),
        ('rf', rf)
    ])
    mor_ensemble = MultiOutputRegressor(ensemble_model)
    mor_ensemble.fit(X_train, y_train)

    # Predictions
    y_pred_ensemble = mor_ensemble.predict(X_test)

    # Evaluate
    print("\nEnsemble Model Results (Gradient Boosting + Kernelized SVR + Random Forest):")
    print("MSE:", mean_squared_error(y_test, y_pred_ensemble, multioutput='uniform_average'))
    print("R²:", round(r2_score(y_test, y_pred_ensemble, multioutput='uniform_average') * 100, 4), "%")

    # Evaluate individual R² scores for each output variable
    print("\nIndividual R² Scores:")
    individual_r2_scores = r2_score(y_test, y_pred_ensemble, multioutput='raw_values')
    for i, r2 in enumerate(individual_r2_scores):
        print(f"R² for target {y.columns[i]}: {round(r2 * 100, 4)}%")



# def run_models():
#     # Feature Engineering
#     # version_one()  # Apply feature transformations

#     # Compute angular momentum components
#     X['h_x'] = X['y'] * X['vz'] - X['z'] * X['vy']
#     X['h_y'] = X['z'] * X['vx'] - X['x'] * X['vz']
#     X['h_z'] = X['x'] * X['vy'] - X['y'] * X['vx']

#     # Magnitude of angular momentum
#     X['h_mag'] = np.sqrt(X['h_x']**2 + X['h_y']**2 + X['h_z']**2)

#     # Position and velocity magnitudes
#     X['r_mag'] = np.sqrt(X['x']**2 + X['y']**2 + X['z']**2)
#     X['v_mag'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)

#     # Compute eccentricity vector components
#     mu = 398600  # Adjust gravitational parameter as necessary
#     X['e_x'] = (X['vy'] * X['h_z'] - X['vz'] * X['h_y']) / mu - X['x'] / X['r_mag']
#     X['e_y'] = (X['vz'] * X['h_x'] - X['vx'] * X['h_z']) / mu - X['y'] / X['r_mag']
#     X['e_z'] = (X['vx'] * X['h_y'] - X['vy'] * X['h_x']) / mu - X['z'] / X['r_mag']

#     # Eccentricity magnitude
#     X['e_mag'] = np.sqrt(X['e_x']**2 + X['e_y']**2 + X['e_z']**2)

#     # Compute inclination
#     X['incl'] = np.arccos(X['h_z'] / X['h_mag'])

#     # Compute true anomaly (ν)
#     X['nu'] = np.arccos((X['x'] * X['e_x'] + X['y'] * X['e_y'] + X['z'] * X['e_z']) / (X['r_mag'] * X['e_mag']))

#     # Semi-major axis
#     X['semi_major_axis'] = 1 / ((2 / X['r_mag']) - (X['v_mag']**2 / mu))

#     # Periastron distance
#     X['r_p'] = X['semi_major_axis'] * (1 - X['e_mag'])


#     # Train/test split
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=33)
#     print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")

#     # Standardize features
#     # scaler = StandardScaler()
#     # X_train = scaler.fit_transform(X_train)
#     # X_test = scaler.transform(X_test)

#     # 1. Support Vector Regression (SVR)
#     print("\n--- Support Vector Regression (SVR) ---")
#     svr = SVR(kernel='poly', degree=5, C=10, epsilon=0.1, gamma='scale')  # Tune these parameters
#     mor_svr = MultiOutputRegressor(svr)
#     mor_svr.fit(X_train, y_train)
#     y_pred_svr = mor_svr.predict(X_test)
#     evaluate_model("SVR", y_test, y_pred_svr)

#     # 2. Gradient Boosting Regressor
#     print("\n--- Gradient Boosting Regressor (GBR) ---")
#     gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)
#     mor_gbr = MultiOutputRegressor(gbr)
#     mor_gbr.fit(X_train, y_train)
#     y_pred_gbr = mor_gbr.predict(X_test)
#     evaluate_model("Gradient Boosting", y_test, y_pred_gbr)

#     # 3. Random Forest Regressor
#     print("\n--- Random Forest Regressor (RFR) ---")
#     rfr = RandomForestRegressor(n_estimators=200, max_depth=20, random_state=33)
#     mor_rfr = MultiOutputRegressor(rfr)
#     mor_rfr.fit(X_train, y_train)  # RandomForest doesn't require scaling
#     y_pred_rfr = mor_rfr.predict(X_test)
#     evaluate_model("Random Forest", y_test, y_pred_rfr)

#     # 4. Ensemble Voting Regressor
#     print("\n--- Ensemble Voting Regressor ---")
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


# def evaluate_model(model_name, y_test, y_pred):
#     mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
#     r2 = r2_score(y_test, y_pred, multioutput='uniform_average')
#     print(f"{model_name} - Mean Squared Error (MSE): {mse:.4f}")
#     print(f"{model_name} - R² Score: {r2:.4f}")
#     # Evaluate individual R² scores
#     individual_r2 = r2_score(y_test, y_pred, multioutput='raw_values')
#     for i, r2 in enumerate(individual_r2):
#         print(f"{model_name} - R² for target {y.columns[i]}: {round(r2 * 100, 4)}%")



def run_models(X, y):
    # Handle missing values
    # Handle missing values
    print("Checking for missing values...")
    print(X.isnull().sum())
    print(y.isnull().sum())

    # Impute missing values with mean
    imputer = SimpleImputer(strategy='mean')  # Choose 'median' or another strategy if needed
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    y = pd.DataFrame(imputer.fit_transform(y), columns=y.columns)

    print("Missing values handled. Checking again...")
    print(X.isnull().sum())
    print(y.isnull().sum())

    # Feature Engineering
    epsilon = 1e-8  # Small value to avoid division by zero

    # X['vx2'] = X['vx'] * X['vx']
    # X['vy2'] = X['vy'] * X['vy']
    # X['vz2'] = X['vz'] * X['vz']
    # X['v']=np.sqrt(X['vx2']+X['vy2']+X['vz2'])
    # X['vxvy'] = X['vx'] * X['vy']
    # X['vxvz'] = X['vx'] * X['vz']
    # X['vyvz'] = X['vy'] * X['vz']
    # X['vxvyvz'] = X['vx'] * X['vy'] + X['vy'] * X['vz'] + X['vz'] * X['vx']
    # X['vxvyvz2'] = X['vx'] * X['vx'] + X['vy'] * X['vy'] + X['vz'] * X['vz']
    # X['vx_plus_vy'] = X['vx'] * X['vx'] + X['vy'] * X['vy']
    # X['vx_plus_vz'] = X['vx'] * X['vx'] + X['vz'] * X['vz']
    # X['vy_plus_vz'] = X['vy'] * X['vy'] + X['vz'] * X['vz']
    # X['vx_minus_vy'] = X['vx'] * X['vx'] - X['vy'] * X['vy']
    # X['vx_minus_vz'] = X['vx'] * X['vx'] - X['vz'] * X['vz']
    # X['vy_minus_vz'] = X['vy'] * X['vy'] - X['vz'] * X['vz']
    # X['pl_bmasse_sqrt'] = np.sqrt(X['pl_bmasse']) * np.pow(X['pl_bmasse'], 2)
    # X['pl_bmasse_sqrt'] = np.sqrt(X['pl_bmasse'])
    # X['x2'] = X['x'] * X['x']
    # X['y2'] = X['y'] * X['y']
    # X['z2'] = X['z'] * X['z']
    # X['r'] = np.sqrt(X['x2'] + X['y2'] + X['z2'])
    # X['r2'] = X['x2'] + X['y2'] + X['z2']
    # X['r2O'] = X['r'] * X['r'] * X['pl_Omega'] 
    # X['pl_bmasse']=4.3009e-6*X['pl_bmasse']

    # Compute angular momentum components
    X['h_x'] = X['y'] * X['vz'] - X['z'] * X['vy']
    X['h_y'] = X['z'] * X['vx'] - X['x'] * X['vz']
    X['h_z'] = X['x'] * X['vy'] - X['y'] * X['vx']

    # Magnitude of angular momentum
    X['h_mag'] = np.sqrt(X['h_x']**2 + X['h_y']**2 + X['h_z']**2) + epsilon

    # Position and velocity magnitudes
    X['r_mag'] = np.sqrt(X['x']**2 + X['y']**2 + X['z']**2) + epsilon
    X['v_mag'] = np.sqrt(X['vx']**2 + X['vy']**2 + X['vz']**2)

    # Compute eccentricity vector components
    mu = 398600  # Adjust gravitational parameter as necessary
    X['e_x'] = (X['vy'] * X['h_z'] - X['vz'] * X['h_y']) / mu - X['x'] / X['r_mag']
    X['e_y'] = (X['vz'] * X['h_x'] - X['vx'] * X['h_z']) / mu - X['y'] / X['r_mag']
    X['e_z'] = (X['vx'] * X['h_y'] - X['vy'] * X['h_x']) / mu - X['z'] / X['r_mag']

    # Eccentricity magnitude
    X['e_mag'] = np.sqrt(X['e_x']**2 + X['e_y']**2 + X['e_z']**2) + epsilon

    # Clamp values for inclination and true anomaly
    X['incl'] = np.arccos(np.clip(X['h_z'] / X['h_mag'], -1, 1))
    X['nu'] = np.arccos(np.clip(
        (X['x'] * X['e_x'] + X['y'] * X['e_y'] + X['z'] * X['e_z']) / (X['r_mag'] * X['e_mag'] + epsilon),
        -1, 1
    ))

    # Semi-major axis
    X['semi_major_axis'] = 1 / ((2 / X['r_mag']) - (X['v_mag']**2 / mu))

    # Periastron distance
    X['r_p'] = X['semi_major_axis'] * (1 - X['e_mag'])


    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=33)
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")

    # 1. Support Vector Regression (SVR)
    print("\n--- Support Vector Regression (SVR) ---")
    svr = SVR(kernel='poly', degree=5, C=10, epsilon=0.1, gamma='scale')
    mor_svr = MultiOutputRegressor(svr)
    mor_svr.fit(X_train, y_train)
    y_pred_svr = mor_svr.predict(X_test)
    evaluate_model("SVR", y_test, y_pred_svr)

    # 2. Gradient Boosting Regressor
    print("\n--- Gradient Boosting Regressor (GBR) ---")
    gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)
    mor_gbr = MultiOutputRegressor(gbr)
    mor_gbr.fit(X_train, y_train)
    y_pred_gbr = mor_gbr.predict(X_test)
    evaluate_model("Gradient Boosting", y_test, y_pred_gbr)

    # 3. Random Forest Regressor
    print("\n--- Random Forest Regressor (RFR) ---")
    rfr = RandomForestRegressor(n_estimators=200, max_depth=20, random_state=33)
    mor_rfr = MultiOutputRegressor(rfr)
    mor_rfr.fit(X_train, y_train)
    y_pred_rfr = mor_rfr.predict(X_test)
    evaluate_model("Random Forest", y_test, y_pred_rfr)

    # 4. Ensemble Voting Regressor
    print("\n--- Ensemble Voting Regressor ---")
    voting_regressor = VotingRegressor(
        estimators=[
            ('gbr', GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=33)),
            ('rfr', RandomForestRegressor(n_estimators=200, max_depth=10, random_state=33)),
            ('svr', SVR(kernel='rbf', C=10, epsilon=0.1, gamma='scale'))
        ]
    )
    mor_voting = MultiOutputRegressor(voting_regressor)
    mor_voting.fit(X_train, y_train)
    y_pred_voting = mor_voting.predict(X_test)
    evaluate_model("Voting Regressor", y_test, y_pred_voting)
    # Save the trained model to a file
    joblib.dump(mor_svr, 'save_models/svr_model.joblib')
    joblib.dump(mor_gbr, 'save_models/gbr_model.joblib')
    joblib.dump(mor_rfr, 'save_models/rfr_model.joblib')
    joblib.dump(mor_voting, 'save_models/voting_regressor_model.joblib')

    print("Models saved successfully.")


def evaluate_model(model_name, y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
    r2 = r2_score(y_test, y_pred, multioutput='uniform_average')
    print(f"{model_name} - Mean Squared Error (MSE): {mse:.4f}")
    print(f"{model_name} - R² Score: {r2:.4f}")
    # Evaluate individual R² scores
    individual_r2 = r2_score(y_test, y_pred, multioutput='raw_values')
    for i, r2 in enumerate(individual_r2):
        print(f"{model_name} - R² for target {y.columns[i]}: {round(r2 * 100, 4)}%")

if __name__ == "__main__":
    # Load your dataset into X (features) and y (target variables)
    # Example:
    # X = pd.read_csv('your_features.csv')
    # y = pd.read_csv('your_targets.csv')
    # Ensure X and y are clean and aligned

    run_models(X, y)



# if __name__ == "__main__":
#     # version_one()
#     run_models()
#     # version_two()  # Use this for the ensemble model with multiple outputs  