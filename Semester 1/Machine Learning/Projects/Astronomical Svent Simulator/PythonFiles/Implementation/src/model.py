# import os
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
# from sklearn.impute import SimpleImputer
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.model_selection import GridSearchCV, train_test_split
# from sklearn.multioutput import MultiOutputRegressor
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.svm import SVR
# from xgboost import XGBRegressor

# # def load_data(dir_path):
# #     # Load the data from the CSV file
# #     list_csv = os.listdir(dir_path)
# #     X = pd.DataFrame()
# #     Y = pd.DataFrame()
# #     for file in list_csv:
# #         df = pd.read_csv(os.path.join(dir_path, file))
# #         name = file.split('.')[0]
# #         X[name] = df.iloc[:351].squeeze()
# #         Y[name] = df.iloc[352:].squeeze()
    
# #     return X, Y


# def load_data(dir_path):
#     """Load multiple CSV files from a directory and split data into features (X) and targets (Y)."""
#     list_csv = os.listdir(dir_path)
#     list_csv = [os.path.join(dir_path, file) for file in list_csv if file.endswith('.csv')]
#     # print(f"list_csv:{list_csv}")
#     feature_list = []
#     target_list = []
#     n = 10
#     dt = int(86400/200)
#     big_df=pd.DataFrame(index=range(n),columns=range(707))
#     print(f"big_df.shape:{big_df.shape}")
#     one_big_row=[]

#     df = [None] * len(list_csv)
#     old_read_rows=0
#     for j in range(n):
#         for i,file in enumerate(list_csv):
#             df[i]=pd.read_csv(file,skiprows=old_read_rows,nrows=1)
#         big_df.iloc[j:j+1,:]=pd.concat([df[i] for i in range(len(list_csv))],axis=1)
#         # big_df.iloc[j:j+1, 'dt'] = dt
#         # big_df['dt'][j] = dt
#         # print(big_df.iloc[j,:])
#         # print(pd.concat([df[i] for i in range(len(list_csv))],axis=1))
#         old_read_rows+=1

#     print(big_df.shape)

#     # one_big_row.append(df[i].iloc[:,:])
#     # for file_var in list_csv:
#     #     big_df.ilo=
#     # for i in range(400):
#     #     file_path = os.path.join(dir_path, file)
#     #     df = pd.read_csv(file_path,skiprows=i,nrows=1)



#     # for file in list_csv:
#     #     file_path = os.path.join(dir_path, file)
#     #     df = pd.read_csv(file_path)
#     #     train_list = []
#     #     tar_list = []
#     #     for i, row in df.iterrows():
#     #         if i < 351:
#     #             train_list.append(row.to_list())
#     #         else:
#     #             tar_list.append(row.to_list())

#     #     feature_list.append(train_list)
#     #     target_list.append(tar_list)

#     # # Combine all loaded data into DataFrames
#     # X = pd.DataFrame(np.asanyarray(feature_list))
#     # Y = pd.DataFrame(np.asanyarray(target_list))
#     # print(X)
#     X = big_df.iloc[:-1,:]
#     Y = big_df.iloc[1:,:]

#     return X,Y



# def feature_engineering(X, y):
#     pass

# def run_models(X, y):
#     imputer = SimpleImputer(strategy='mean')
#     X = imputer.fit_transform(X)
#     y = imputer.fit_transform(y)

#     feature_scaler = MinMaxScaler()
#     target_scaler = MinMaxScaler()
    
#     X = feature_scaler.fit_transform(X)
#     y = target_scaler.fit_transform(y)

#     # Grid Search Hyper Tuning
#     param_grid = {
#         'learning_rate': [0.01, 0.1, 0.2],
#         'max_depth': [3, 5, 7],
#         'n_estimators': [100, 200],
#         # 'subsample': [0.8, 0.9, 1.0],
#         'subsample': [0.8,],
#         'colsample_bytree': [0.8],
#         # 'gamma': [0, 0.1, 0.2]  # Regularization parameter
#     }

#     # Train/test split
#     print("+------------------+------------------------------------------++")
#     print("| Train-Test-Split |------------------------------------------||")
#     print("+------------------+------------------------------------------++")
    
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
#     print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")

#     # 1. Support Vector Regression (SVR)
#     print("+---------------------------------+---------------------------++")
#     print("| Support Vector Regression (SVR) |---------------------------||")
#     print("+---------------------------------+---------------------------++")
#     svr = SVR(kernel='poly', degree=5, C=2, epsilon=0.2, gamma='scale')
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

#     # 3. Xtreme Gradient Boosting Regressor (XGBR)
#     print("+-------------------------------------------+-----------------++")
#     print("| Xtreme Gradient Boosting Regressor (XGBR) |-----------------||")
#     print("+-------------------------------------------+-----------------++")
#     # xgbr = XGBRegressor(n_estimators=120, learning_rate=0.07, max_depth=4, random_state=33)
#     # grid_search = GridSearchCV(XGBRegressor(random_state=42), param_grid, scoring='r2', cv=5)
#     # mor_xgbr = MultiOutputRegressor(grid_search)
#     # # mor_xgbr = MultiOutputRegressor(xgbr)
#     # # Train the model with grid search
#     # mor_xgbr.fit(X_train, y_train)
#     # y_pred_xgbr = mor_xgbr.predict(X_test)
#     # evaluate_model("XGBoost", y_test, y_pred_xgbr)

#     # Initialize GridSearchCV with XGBRegressor
#     base_xgbr = XGBRegressor(random_state=42)
#     grid_search = GridSearchCV(base_xgbr, param_grid, scoring='r2', cv=5)

#     # Perform GridSearchCV for each target variable independently
#     best_models = []
#     for i in range(y_train.shape[1]):
#         print(f"Grid search for target {i + 1}/{y_train.shape[1]}...")
#         grid_search.fit(X_train, y_train[:, i])
#         best_models.append(grid_search.best_estimator_)
    
#     # Create a MultiOutputRegressor using the best models from GridSearchCV
#     mor_xgbr = MultiOutputRegressor(estimator=base_xgbr)
#     mor_xgbr.estimators_ = best_models  # Manually set the best estimators
#     y_pred_xgbr = mor_xgbr.predict(X_test)

#     evaluate_model("XGBoost", y_test, y_pred_xgbr)



#     # 5. Random Forest Regressor (RFR)
#     print("+-------------------------------+-----------------------------++")
#     print("| Random Forest Regressor (RFR) |-----------------------------||")
#     print("+-------------------------------+-----------------------------++")
#     rfr = RandomForestRegressor(n_estimators=300, max_depth=10, random_state=33)
#     mor_rfr = MultiOutputRegressor(rfr)
#     mor_rfr.fit(X_train, y_train)
#     y_pred_rfr = mor_rfr.predict(X_test)
#     evaluate_model("Random Forest", y_test, y_pred_rfr)

#     # 6. Ensemble Voting Regressor (EVR)
#     print("+---------------------------------+--------------------------++")
#     print("| Ensemble Voting Regressor (EVR) |--------------------------||")
#     print("+---------------------------------+--------------------------++")
#     voting_regressor = VotingRegressor(
#         estimators=[
#             ('gbr', GradientBoostingRegressor(n_estimators=200, learning_rate=0.09, max_depth=4, random_state=33)),
#             ('rfr', RandomForestRegressor(n_estimators=300, max_depth=10, random_state=11)),
#             ('svr', SVR(kernel='rbf', C=10, epsilon=0.2, gamma='scale'))
#         ]
#     )
#     mor_voting = MultiOutputRegressor(voting_regressor)
#     mor_voting.fit(X_train, y_train)
#     y_pred_voting = mor_voting.predict(X_test)
#     evaluate_model("Voting Regressor", y_test, y_pred_voting)

#     # Save the trained models
#     joblib.dump(mor_svr, '../save_models/svr_model.joblib')
#     joblib.dump(mor_gbr, '../save_models/gbr_model.joblib')
#     joblib.dump(mor_xgbr, '../save_models/xgbr_model.joblib')
#     joblib.dump(mor_rfr, '../save_models/rfr_model.joblib')
#     joblib.dump(mor_voting, '../save_models/voting_regressor_model.joblib')

#     print("Models saved successfully.")

# def evaluate_model(model_name, y_test, y_pred):
#     mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
#     r2 = r2_score(y_test, y_pred, multioutput='uniform_average')
#     print(f"{model_name} - Mean Squared Error (MSE): {mse:.4f}")
#     print(f"{model_name} - R² Score: {r2:.4f}")
#     # Evaluate individual R² scores
#     individual_r2 = r2_score(y_test, y_pred, multioutput='raw_values')
#     for i, r2 in enumerate(individual_r2):
#         print(f"{model_name} - R² for target {y.columns[i]}: {round(r2 * 100, 4)}%")



# if __name__ == "__main__":
#     dir_path = '../n_body_100_08_PM_nov_28/'
#     X, y = load_data(dir_path=dir_path)
#     # load_data(dir_path=dir_path)
#     run_models(X, y)
#     # print(X)



# import os
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.base import clone
# from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
# from sklearn.impute import SimpleImputer
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.model_selection import KFold, ParameterGrid
# from sklearn.multioutput import MultiOutputRegressor
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.svm import SVR
# from xgboost import XGBRegressor

# def load_data(dir_path):
    # """Load multiple CSV files from a directory and split data into features (X) and targets (Y)."""
    # # list_csv = [f for f in os.listdir(dir_path) if f.endswith('.csv')]
    # if not os.path.exists(dir_path):
    #     raise ValueError(f"Directory not found: {dir_path}")
    
    # list_csv = [f for f in os.listdir(dir_path) if f.endswith('.csv')]
    # list_csv = [os.path.join(dir_path, file) for file in list_csv]
    # if not list_csv:
    #     raise ValueError(f"No CSV files found in {dir_path}")
        
    # print(f"Found {len(list_csv)} CSV files: {list_csv}")
    
    # n = 400  # Number of rows to read
    # big_df = pd.DataFrame(index=range(n), columns=range(707))
    # dt = int(86400/200)
    # df = [None] * len(list_csv)
    # old_read_rows = 0
    # dt = int(86400/200)
    # for j in range(n):
    #     for i, file in enumerate(list_csv):
    #         df[i] = pd.read_csv(
    #             file, 
    #             skiprows=old_read_rows, 
    #             nrows=1
    #             )
    #     big_df.iloc[j:j+1, :] = pd.concat([df[i] for i in range(len(list_csv))], axis=1)
    #     old_read_rows += 1

    # print(f"Loaded data shape: {big_df.shape}")
    # X = big_df.iloc[:-1, :]
    # X['dt'] = X['dt'].astype(int)
    # Y = big_df.iloc[1:, :]
    
    # return X, Y

# def preprocess_data(X, y):
#     """Preprocess the data with imputation and scaling."""
#     print("\nPreprocessing data...")
#     print(f"Input shapes - X: {X.shape}, y: {y.shape}")
    
#     imputer = SimpleImputer(strategy='mean')
#     X = imputer.fit_transform(X)
#     y = imputer.fit_transform(y)
    
#     feature_scaler = MinMaxScaler()
#     target_scaler = MinMaxScaler()
    
#     X = feature_scaler.fit_transform(X)
#     X['dt'] = X['dt'].astype(int)
#     y = target_scaler.fit_transform(y)
    
#     print(f"After preprocessing - X: {X.shape}, y: {y.shape}")
#     print(f"X range: [{X.min():.2f}, {X.max():.2f}], y range: [{y.min():.2f}, {y.max():.2f}]")
    
#     return X, y, (feature_scaler, target_scaler)

# def create_model_configs():
#     """Create configurations for different models."""
#     # Simplified parameter grids for initial testing
#     xgb_params = {
#         'learning_rate': [0.1],
#         'max_depth': [3],
#         'n_estimators': [100],
#         'subsample': [0.8],
#         'colsample_bytree': [0.8],
#         'min_child_weight': [1]
#     }
    
#     rf_params = {
#         'n_estimators': [200],
#         'max_depth': [10],
#         'min_samples_split': [2],
#         'min_samples_leaf': [1]
#     }
    
#     gbr_params = {
#         'n_estimators': [100],
#         'learning_rate': [0.1],
#         'max_depth': [3],
#         'subsample': [0.8]
#     }
    
#     return {
#         'xgb': (XGBRegressor(random_state=33), xgb_params),
#         'rf': (RandomForestRegressor(random_state=33), rf_params),
#         'gbr': (GradientBoostingRegressor(random_state=33), gbr_params)
#     }

# def train_single_target(X, y_target, base_model, param_grid, target_idx, n_splits=100):
#     """Train model for a single target with cross-validation."""
#     kf = KFold(n_splits=n_splits, shuffle=True, random_state=33)
#     param_list = list(ParameterGrid(param_grid))
    
#     best_score = float('-inf')
#     best_params = None
#     best_model = None
    
#     print(f"\nTraining for target {target_idx + 1}")
#     print(f"Target data shape: {y_target.shape}")
#     print(f"Testing {len(param_list)} parameter combinations")
    
#     for params in param_list:
#         current_scores = []
#         model = clone(base_model)
#         model.set_params(**params)
        
#         try:
#             for train_idx, val_idx in kf.split(X):
#                 X_train, X_val = X[train_idx], X[val_idx]
#                 y_train, y_val = y_target[train_idx], y_target[val_idx]
                
#                 model.fit(X_train, y_train)
#                 y_pred = model.predict(X_val)
#                 score = r2_score(y_val, y_pred)
#                 current_scores.append(score)
            
#             avg_score = np.mean(current_scores)
#             print(f"Parameters: {params}")
#             print(f"Average R² score: {avg_score:.4f}")
            
#             if avg_score > best_score:
#                 best_score = avg_score
#                 best_params = params
#                 best_model = clone(base_model).set_params(**params)
#                 best_model.fit(X, y_target)  # Fit on all data
                
#         except Exception as e:
#             print(f"Error during training with parameters {params}: {str(e)}")
#             continue
    
#     return best_model, best_params, best_score

# def train_model_with_kfold(X, y, base_model, param_grid, n_splits=25):
#     """Train a model using k-fold cross validation for multiple targets."""
#     print(f"\nStarting k-fold training with {n_splits} splits")
#     print(f"Data shapes - X: {X.shape}, y: {y.shape}")
    
#     best_models = []
#     best_params_list = []
#     best_scores = []
    
#     for i in range(y.shape[1]):
#         y_target = y[:, i]
#         model, params, score = train_single_target(X, y_target, base_model, param_grid, i, n_splits)
        
#         if model is not None:
#             best_models.append(model)
#             best_params_list.append(params)
#             best_scores.append(score)
#             print(f"Target {i + 1}: Best score = {score:.4f}, Best params = {params}")
#         else:
#             print(f"Warning: No valid model found for target {i + 1}")
#             # Use default parameters as fallback
#             default_model = clone(base_model)
#             default_model.fit(X, y_target)
#             best_models.append(default_model)
#             best_params_list.append(base_model.get_params())
#             best_scores.append(float('-inf'))
    
#     # Create final multi-output model using the best parameters found
#     if len(best_params_list) > 0:
#         # Use the parameters that gave the best average performance
#         best_idx = np.argmax(best_scores)
#         final_model = MultiOutputRegressor(clone(base_model).set_params(**best_params_list[best_idx]))
#         final_model.fit(X, y)
#     else:
#         print("Warning: Using default parameters for final model")
#         final_model = MultiOutputRegressor(base_model)
#         final_model.fit(X, y)
    
#     return final_model, best_models

# def evaluate_models(X, y, models, model_names, n_splits=25):
#     """Evaluate models using k-fold cross validation."""
#     kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
#     for name, model in zip(model_names, models):
#         print(f"\nEvaluating {name}")
#         r2_scores = []
#         mse_scores = []
        
#         for train_idx, val_idx in kf.split(X):
#             X_val = X[val_idx]
#             y_val = y[val_idx]
            
#             y_pred = model.predict(X_val)
#             r2_scores.append(r2_score(y_val, y_pred, multioutput='uniform_average'))
#             mse_scores.append(mean_squared_error(y_val, y_pred, multioutput='uniform_average'))
        
#         print(f"Average R² Score: {np.mean(r2_scores):.4f} (±{np.std(r2_scores):.4f})")
#         print(f"Average MSE: {np.mean(mse_scores):.4f} (±{np.std(mse_scores):.4f})")

# def main():
#     print("Starting model training pipeline...")
    
#     # Load and preprocess data
#     dir_path = '../n_body_100_08_PM_nov_28/'
#     X, y = load_data(dir_path)
#     X, y, scalers = preprocess_data(X, y)
    
#     # Create and train models
#     model_configs = create_model_configs()
#     trained_models = {}
#     best_models = {}
    
#     for name, (model, params) in model_configs.items():
#         print(f"\nTraining {name} model")
#         trained_models[name], best_models[name] = train_model_with_kfold(X, y, model, params)
    
#     # Evaluate models
#     evaluate_models(
#         X, y,
#         [trained_models[name] for name in model_configs.keys()],
#         list(model_configs.keys())
#     )
    
#     # Create and evaluate voting regressor
#     voting_reg = VotingRegressor([
#         (name, model) for name, model in trained_models.items()
#     ])
#     voting_reg.fit(X, y)
    
#     # Save models
#     save_dir = '../save_models/'
#     os.makedirs(save_dir, exist_ok=True)
    
#     for name, model in trained_models.items():
#         joblib.dump(model, os.path.join(save_dir, f'{name}_model.joblib'))
#     joblib.dump(voting_reg, os.path.join(save_dir, 'voting_regressor_model.joblib'))
#     joblib.dump(scalers, os.path.join(save_dir, 'scalers.joblib'))
    
#     print("\nAll models saved successfully.")

# if __name__ == "__main__":
#     main()

# ================================== TAB 1 ==================================
'''
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold, ParameterGrid
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

def load_data(dir_path):
    """Efficiently load and concatenate multiple CSV files into a single DataFrame."""
    if not os.path.exists(dir_path):
        raise ValueError(f"Directory not found: {dir_path}")
    
    csv_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
    if not csv_files:
        raise ValueError(f"No CSV files found in {dir_path}")
    
    print(f"Found {len(csv_files)} CSV files")
    # Load all CSV files and concatenate
    df_list = [pd.read_csv(file) for file in csv_files]
    big_df = pd.concat(df_list, axis=1)
    
    print(f"Loaded data shape: {big_df.shape}")
    X = big_df.iloc[:-1, :].reset_index(drop=True)
    y = big_df.iloc[1:, :].reset_index(drop=True)
    dt = int(86400/200) #   * X.shape[0]
    X['dt'] = dt
    print(f"X shape: {X.shape};  Y shape: {y.shape}")
    return X, y

def preprocess_data(X, y):
    """Preprocess the data with imputation and scaling."""
    print("\nPreprocessing data...")
    print(f"Input shapes - X: {X.shape}, y: {y.shape}")
    
    imputer = SimpleImputer(strategy='mean')
    scaler = MinMaxScaler()
    
    X = imputer.fit_transform(X)
    y = imputer.fit_transform(y)
    
    X = scaler.fit_transform(X)
    y = scaler.fit_transform(y)
    
    print(f"After preprocessing - X: {X.shape}, y: {y.shape}")
    return X, y, scaler

def create_model_configs():
    """Define simplified parameter grids for models."""
    xgb_params = {
        'learning_rate': [0.1],
        'max_depth': [3],
        'n_estimators': [100],
    }
    rf_params = {
        'n_estimators': [200],
        'max_depth': [10],
    }
    gbr_params = {
        'n_estimators': [100],
        'learning_rate': [0.1],
        'max_depth': [3],
    }
    return {
        'xgb': (XGBRegressor(n_jobs=-1, random_state=33), xgb_params),
        'rf': (RandomForestRegressor(n_jobs=-1, random_state=33), rf_params),
        'gbr': (GradientBoostingRegressor(random_state=33), gbr_params)
    }

def train_and_evaluate(X, y, model_configs, n_splits=5):
    """Train models with k-fold cross-validation and return the best models."""
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=33)
    trained_models = {}
    
    for name, (base_model, param_grid) in model_configs.items():
        print(f"\nTraining {name} model")
        best_model, best_score = None, float('-inf')
        param_list = list(ParameterGrid(param_grid))
        
        for params in param_list:
            model = MultiOutputRegressor(clone(base_model).set_params(**params), n_jobs=-1)
            scores = []
            
            for train_idx, val_idx in kf.split(X):
                X_train, X_val = X[train_idx], X[val_idx]
                y_train, y_val = y[train_idx], y[val_idx]
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_val)
                scores.append(r2_score(y_val, y_pred, multioutput='uniform_average'))
            
            avg_score = np.mean(scores)
            print(f"Params: {params} - R² Score: {avg_score:.4f}")
            
            if avg_score > best_score:
                best_model, best_score = model, avg_score
        
        trained_models[name] = best_model
        print(f"Best R² Score for {name}: {best_score:.4f}")
    
    return trained_models

def main():
    dir_path = '../n_body_100_08_PM_nov_28/'
    X, y = load_data(dir_path)
    X, y, scaler = preprocess_data(X, y)
    
    model_configs = create_model_configs()
    trained_models = train_and_evaluate(X, y, model_configs)
    
    save_dir = '../save_models/'
    os.makedirs(save_dir, exist_ok=True)
    
    for name, model in trained_models.items():
        joblib.dump(model, os.path.join(save_dir, f'{name}_model.joblib'))
    joblib.dump(scaler, os.path.join(save_dir, 'scaler.joblib'))
    
    print("\nModels saved successfully.")

if __name__ == "__main__":
    main()
'''

# ===================================== TAB 2 =====================================

import os
import joblib
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

def parallel_load_csv(file_path):
    return pd.read_csv(file_path)

def load_data(dir_path):
    if not os.path.exists(dir_path):
        raise ValueError(f"Directory not found: {dir_path}")
    
    csv_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
    if not csv_files:
        raise ValueError(f"No CSV files found in {dir_path}")
    
    with ProcessPoolExecutor() as executor:
        df_list = list(executor.map(parallel_load_csv, csv_files))
    
    big_df = pd.concat(df_list, axis=1)
    X = big_df.iloc[:-1, :].reset_index(drop=True)
    y = big_df.iloc[1:, :].reset_index(drop=True)
    X['dt'] = int(86400/200)
    return X, y

def preprocess_data(X, y):
    imputer = SimpleImputer(strategy='mean')
    scaler = MinMaxScaler()
    
    X = imputer.fit_transform(X)
    y = imputer.fit_transform(y)
    X = scaler.fit_transform(X)
    y = scaler.fit_transform(y)
    
    return X, y, scaler

def train_model(X, y, n_splits=3):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=33)
    
    voting_regressor = VotingRegressor([
        ('xgb', XGBRegressor(learning_rate=0.1, max_depth=3, n_estimators=100, n_jobs=-1)),
        ('rf', RandomForestRegressor(n_estimators=200, max_depth=10, n_jobs=-1)),
        ('gbr', GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3))
    ], n_jobs=-1)
    
    model = MultiOutputRegressor(voting_regressor, n_jobs=-1)
    scores = []
    
    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        scores.append(r2_score(y_val, y_pred, multioutput='uniform_average'))
    
    return model, np.mean(scores)

def main():
    dir_path = '../n_body_100_08_PM_nov_28/'
    save_dir = '../save_models/'
    os.makedirs(save_dir, exist_ok=True)
    
    X, y = load_data(dir_path)
    X, y, scaler = preprocess_data(X, y)
    model, score = train_model(X, y)
    
    joblib.dump(model, os.path.join(save_dir, 'ensemble_model.joblib'))
    joblib.dump(scaler, os.path.join(save_dir, 'scaler.joblib'))
    print(f"Training complete. Final R² Score: {score:.4f}")

if __name__ == "__main__":
    main()


# ===================================== OLD CODE =====================================


# import os
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.base import clone
# from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
# from sklearn.impute import SimpleImputer
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.model_selection import KFold, ParameterGrid
# from sklearn.multioutput import MultiOutputRegressor
# from sklearn.preprocessing import MinMaxScaler
# from xgboost import XGBRegressor

# def load_data(dir_path):
#     """Load multiple CSV files from a directory and split data into features (X) and targets (Y)."""
#     if not os.path.exists(dir_path):
#         raise ValueError(f"Directory not found: {dir_path}")
    
#     list_csv = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
#     if not list_csv:
#         raise ValueError(f"No CSV files found in {dir_path}")
        
#     print(f"Found {len(list_csv)} CSV files.")
    
#     n = 400  # Number of rows to read
#     big_df = []
#     old_read_rows = 0
    
#     for j in range(n):
#         row_data = []
#         for file in list_csv:
#             # DEBUG: 
#             print(f"Reading {file}")
#             data = pd.read_csv(file, skiprows=old_read_rows, nrows=1)
#             row_data.append(data.values.flatten())
#         big_df.append(np.concatenate(row_data))
#         old_read_rows += 1

#     big_df = pd.DataFrame(big_df)
#     print(f"Loaded data shape: {big_df.shape}")
    
#     X = big_df.iloc[:-1, :].values
#     Y = big_df.iloc[1:, :].values
    
#     return X, Y

# def preprocess_data(X, y):
#     """Preprocess the data with imputation and scaling."""
#     print("\nPreprocessing data...")
    
#     imputer = SimpleImputer(strategy='mean')
#     X = imputer.fit_transform(X)
#     y = imputer.fit_transform(y)
    
#     feature_scaler = MinMaxScaler()
#     target_scaler = MinMaxScaler()
    
#     X = feature_scaler.fit_transform(X)
#     y = target_scaler.fit_transform(y)
    
#     print(f"Preprocessed data shapes - X: {X.shape}, y: {y.shape}")
#     print(f"X_data : {X}")
#     print(f"Y_data : {y}")
#     return X, y, (feature_scaler, target_scaler)

# def create_model_configs():
#     """Create configurations for different models."""
#     xgb_params = {
#         'learning_rate': [0.1],
#         'max_depth': [3],
#         'n_estimators': [100],
#         'subsample': [0.8],
#         'colsample_bytree': [0.8],
#         'min_child_weight': [1]
#     }
#     rf_params = {
#         'n_estimators': [200],
#         'max_depth': [10],
#         'min_samples_split': [2],
#         'min_samples_leaf': [1]
#     }
#     gbr_params = {
#         'n_estimators': [100],
#         'learning_rate': [0.1],
#         'max_depth': [3],
#         'subsample': [0.8]
#     }
#     return {
#         'xgb': (XGBRegressor(random_state=42), xgb_params),
#         'rf': (RandomForestRegressor(random_state=42), rf_params),
#         'gbr': (GradientBoostingRegressor(random_state=42), gbr_params)
#     }


# def train_single_target(X, y_target, base_model, param_grid, target_idx, n_splits=25):
#     """Train model for a single target with cross-validation."""
#     kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
#     param_list = list(ParameterGrid(param_grid))
    
#     best_score = float('-inf')
#     best_params = None
#     best_model = None
    
#     print(f"\nTraining for target {target_idx + 1}")
#     print(f"Target data shape: {y_target.shape}")
#     print(f"Testing {len(param_list)} parameter combinations")
    
#     for params in param_list:
#         current_scores = []
#         model = clone(base_model)
#         model.set_params(**params)
        
#         try:
#             for train_idx, val_idx in kf.split(X):
#                 X_train, X_val = X[train_idx], X[val_idx]
#                 y_train, y_val = y_target[train_idx], y_target[val_idx]
                
#                 model.fit(X_train, y_train)
#                 y_pred = model.predict(X_val)
#                 score = r2_score(y_val, y_pred)
#                 current_scores.append(score)
            
#             avg_score = np.mean(current_scores)
#             print(f"Parameters: {params}")
#             print(f"Average R² score: {avg_score:.4f}")
            
#             if avg_score > best_score:
#                 best_score = avg_score
#                 best_params = params
#                 best_model = clone(base_model).set_params(**params)
#                 best_model.fit(X, y_target)  # Fit on all data
                
#         except Exception as e:
#             print(f"Error during training with parameters {params}: {str(e)}")
#             continue
    
#     return best_model, best_params, best_score

# def train_model_with_kfold(X, y, base_model, param_grid, n_splits=25):
#     """Train a model using k-fold cross validation for multiple targets."""
#     print(f"\nStarting k-fold training with {n_splits} splits")
#     print(f"Data shapes - X: {X.shape}, y: {y.shape}")
    
#     best_models = []
#     best_params_list = []
#     best_scores = []
    
#     for i in range(y.shape[1]):
#         y_target = y[:, i]
#         model, params, score = train_single_target(X, y_target, base_model, param_grid, i, n_splits)
        
#         if model is not None:
#             best_models.append(model)
#             best_params_list.append(params)
#             best_scores.append(score)
#             print(f"Target {i + 1}: Best score = {score:.4f}, Best params = {params}")
#         else:
#             print(f"Warning: No valid model found for target {i + 1}")
#             # Use default parameters as fallback
#             default_model = clone(base_model)
#             default_model.fit(X, y_target)
#             best_models.append(default_model)
#             best_params_list.append(base_model.get_params())
#             best_scores.append(float('-inf'))
    
#     # Create final multi-output model using the best parameters found
#     if len(best_params_list) > 0:
#         # Use the parameters that gave the best average performance
#         best_idx = np.argmax(best_scores)
#         final_model = MultiOutputRegressor(clone(base_model).set_params(**best_params_list[best_idx]))
#         final_model.fit(X, y)
#     else:
#         print("Warning: Using default parameters for final model")
#         final_model = MultiOutputRegressor(base_model)
#         final_model.fit(X, y)
    
#     return final_model, best_models

# def evaluate_models(X, y, models, model_names, n_splits=25):
#     """Evaluate models using k-fold cross validation."""
#     kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
#     for name, model in zip(model_names, models):
#         print(f"\nEvaluating {name}")
#         r2_scores = []
#         mse_scores = []
        
#         for train_idx, val_idx in kf.split(X):
#             X_val = X[val_idx]
#             y_val = y[val_idx]
            
#             y_pred = model.predict(X_val)
#             r2_scores.append(r2_score(y_val, y_pred, multioutput='uniform_average'))
#             mse_scores.append(mean_squared_error(y_val, y_pred, multioutput='uniform_average'))
        
#         print(f"Average R² Score: {np.mean(r2_scores):.4f} (±{np.std(r2_scores):.4f})")
#         print(f"Average MSE: {np.mean(mse_scores):.4f} (±{np.std(mse_scores):.4f})")

# def main():
#     print("Starting model training pipeline...")
    
#     # Load and preprocess data
#     dir_path = '../n_body_100_08_PM_nov_28/'
#     X, y = load_data(dir_path)
#     X, y, scalers = preprocess_data(X, y)
    
#     # Create and train models
#     model_configs = create_model_configs()
#     trained_models = {}
#     best_models = {}
    
#     for name, (model, params) in model_configs.items():
#         print(f"\nTraining {name} model")
#         trained_models[name], best_models[name] = train_model_with_kfold(X, y, model, params)
    
#     # Evaluate models
#     evaluate_models(
#         X, y,
#         [trained_models[name] for name in model_configs.keys()],
#         list(model_configs.keys())
#     )
    
#     # Create and evaluate voting regressor
#     voting_reg = VotingRegressor([
#         (name, model) for name, model in trained_models.items()
#     ])
#     voting_reg.fit(X, y)
    
#     # Save models
#     save_dir = '../save_models/'
#     os.makedirs(save_dir, exist_ok=True)
    
#     for name, model in trained_models.items():
#         joblib.dump(model, os.path.join(save_dir, f'{name}_model.joblib'))
#     joblib.dump(voting_reg, os.path.join(save_dir, 'voting_regressor_model.joblib'))
#     joblib.dump(scalers, os.path.join(save_dir, 'scalers.joblib'))
    
#     print("\nAll models saved successfully.")

# if __name__ == "__main__":
#     main()