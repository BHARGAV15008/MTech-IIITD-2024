# # We have this type of datasets train.csv
# id,CustomerId,Surname,CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited
# 0,15570087.0,Chigozie,571.0,Germany,Female,42.0,4.0,127290.61,1.0,1.0,1.0,25669.1,0.0
# 1,15809837.0,Chubb,558.0,France,Male,38.0,2.0,0.0,1.0,1.0,1.0,138849.06,0.0
# 2,15766776.0,Ch'ien,644.0,France,Female,44.0,3.0,0.0,1.0,1.0,0.0,121408.46,1.0
# 3,15649536.0,Chikelu,714.0,France,Female,27.0,6.0,0.0,2.0,1.0,0.0,121151.1,0.0
# 4,15637644.0,Cremonesi,676.0,Spain,Female,33.0,8.0,0.0,2.0,0.0,1.0,170392.59,0.0
# 5,15662908.0,Y?,561.0,France,Male,30.0,1.0,0.0,2.0,1.0,0.0,44335.54,0.0
# 6,15773852.0,Oluchukwu,645.0,France,Female,41.0,1.0,0.0,1.0,1.0,0.0,81452.29,1.0
# 7,15747534.0,Chinomso,607.0,France,Female,34.0,10.0,0.0,2.0,1.0,0.0,111342.66,0.0
# 8,15757895.0,DeRose,687.0,France,Female,35.0,5.0,99610.92,1.0,1.0,1.0,107815.31,0.0
# 9,15592578.0,Walker,642.0,Germany,Female,42.0,3.0,104015.54,1.0,1.0,0.0,159334.93,1.0
# 10,15783629.0,Rizzo,678.0,France,Male,38.0,9.0,0.0,2.0,0.0,0.0,179631.85,0.0

# # We have this type of datasets test.csv
# id,CustomerId,Surname,CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary
# 15000,15767954.0,Smith,701.0,France,Female,33.0,10.0,0.0,2.0,1.0,0.0,62402.38
# 15001,15641110.0,Ch'ang,757.0,France,Male,32.0,10.0,104469.58,1.0,1.0,1.0,63795.8
# 15002,15589496.0,Chukwujekwu,613.0,France,Male,34.0,4.0,0.0,2.0,1.0,0.0,136983.77
# 15003,15777892.0,Nkemjika,684.0,France,Female,41.0,8.0,0.0,2.0,1.0,1.0,147090.9
# 15004,15652914.0,Lucciano,648.0,Spain,Male,38.0,2.0,0.0,2.0,1.0,1.0,54495.82
# 15005,15632576.0,Chidiegwu,663.0,Germany,Female,44.0,1.0,127847.86,1.0,1.0,0.0,103726.71
# 15006,15734999.0,Chukwudi,624.0,France,Female,51.0,8.0,0.0,3.0,1.0,0.0,187985.85
# 15007,15813916.0,Chukwufumnanya,627.0,France,Male,31.0,5.0,0.0,2.0,1.0,1.0,161465.31
# 15008,15681180.0,Chiemenam,464.0,Germany,Female,43.0,0.0,124576.65,1.0,1.0,0.0,80190.36
# 15009,15596713.0,Chiang,718.0,France,Male,36.0,2.0,0.0,2.0,1.0,0.0,162643.15
# 15010,15773971.0,T'ien,686.0,France,Male,35.0,2.0,0.0,2.0,0.0,1.0,110114.19
# 15011,15780142.0,Mazzi,641.0,Germany,Female,51.0,1.0,102827.44,1.0,1.0,1.0,159418.1

# Classificaion models hyper paramenter is here declared by grid class and random class
class GridSearchHP:
    """
    Grid Search on Hyper Parameters for Classification
    """
    def __init__(self, model, hyperparameters) -> None:
        self.model = model
        self.hyperparameters = hyperparameters

    def gradient_boosting_classifier(self) -> None:
        """
        Gradient Boosting Classifier parameters are defined here
        """
        gradient_boosting_param_grid = {
            'learning_rate': [0.01, 0.1, 1],
            'n_estimators': [10, 50, 100],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 5, 10],
            'subsample': [0.5, 0.8, 1],
            'max_features': ['auto', 'sqrt', 'log2']
        }
        self.model = GridSearchHP(self.model, gradient_boosting_param_grid)

    def random_forest_classifier(self) -> None:
        """
        Random Forest Classifier parameters are defined here
        """
        random_forest_param_grid = {
            'n_estimators': [10, 50, 100],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 5, 10],
            'max_features': ['auto', 'sqrt', 'log2']
        }
        self.model = GridSearchHP(self.model, random_forest_param_grid)

    def support_vector_classifier(self) -> None:
        """
        Support Vector Classifier parameters are defined here
        """
        support_vector_param_grid = {
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'C': [0.1, 1, 10],
            'gamma': ['scale', 'auto'],
            'degree': [2, 3, 4],
            'coef0': [0.0, 1.0, 2.0]
        }
        self.model = GridSearchHP(self.model, support_vector_param_grid)

    def xgboost_classifier(self) -> None:
        """
        XGBoost Classifier parameters are defined here
        """
        xgboost_param_grid = {
            'max_depth': [3, 5, 10],
            'learning_rate': [0.01, 0.1, 1],
            'n_estimators': [10, 50, 100],
            'gamma': [0, 0.1, 0.5],
            'subsample': [0.5, 0.8, 1],
            'colsample_bytree': [0.5, 0.8, 1],
            'reg_alpha': [0, 0.1, 0.5],
            'reg_lambda': [0, 0.1, 0.5]
        }
        self.model = GridSearchHP(self.model, xgboost_param_grid)

    def kernel_ridge_classifier(self) -> None:
        """
        Kernel Ridge Classifier parameters are defined here
        """
        kernel_ridge_param_grid = {
            'alpha': [0.1, 1, 10],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'degree': [2, 3, 4],
            'coef0': [0.0, 1.0, 2.0]
        }
        self.model = GridSearchHP(self.model, kernel_ridge_param_grid)

    def light_gradient_classifier(self) -> None:
        """
        Light Gradient Boosting Classifier parameters are defined here
        """
        light_gradient_param_grid = {
            'boosting_type': ['gbdt', 'dart'],
            'num_leaves': [31, 62, 127],
            'learning_rate': [0.01, 0.1, 1],
            'n_estimators': [10, 50, 100],
            'max_depth': [3, 5, 10],
            'min_data_in_leaf': [10, 50, 100],
            'min_sum_hessian_in_leaf': [0.001, 0.01, 0.1],
            'lambda_l1': [0, 0.1, 0.5],
            'lambda_l2': [0, 0.1, 0.5],
            'feature_fraction': [0.5, 0.8, 1],
            'bagging_fraction': [0.5, 0.8, 1],
            'bagging_freq': [0, 1, 2],
            'early_stopping_round': [5, 10, 20]
        }
        self.model = GridSearchHP(self.model, light_gradient_param_grid)

    def knn_classifier(self) -> None:
        """
        K Nearest Neighbors Classifier parameters are defined here
        """
        knn_param_grid = {
            'n_neighbors': [3, 5, 10],
            'weights': ['uniform', 'distance'],
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
            'leaf_size': [10, 30, 50],
            'p': [1, 2]
        }
        self.model = GridSearchHP(self.model, knn_param_grid)

    def bayesian_linear_classifier(self) -> None:
        """
        Bayesian Linear Classifier parameters are defined here
        """
        bayesian_linear_param_grid = {
            'alpha_1': [0.1, 1, 10],
            'alpha_2': [0.1, 1, 10],
            'lambda_1': [0.1, 1, 10],
            'lambda_2': [0.1, 1, 10],
            'fit_intercept': [True, False]
        }
        self.model = GridSearchHP(self.model, bayesian_linear_param_grid)


class RandomizedSearchHP:
    """
    Random Search on Hyper Parameters for Classification
    """
    def __init__(self, model, random_state, n_iter) -> None:
        self.model = model
        self.random_state = random_state
        self.n_iter = n_iter

    def gradient_boosting_classifier(self) -> None:
        """
        Gradient Boosting Classifier parameters are defined here
        """
        gradient_boosting_param_grid = {
            'learning_rate': [0.01, 0.1, 1],
            'n_estimators': [10, 50, 100],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 5, 10],
            'subsample': [0.5, 0.8, 1],
            'max_features': ['auto', 'sqrt', 'log2']
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, gradient_boosting_param_grid)

    def random_forest_classifier(self) -> None:
        """
        Random Forest Classifier parameters are defined here
        """
        random_forest_param_grid = {
            'n_estimators': [10, 50, 100],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 5, 10],
            'max_features': ['auto', 'sqrt', 'log2']
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, random_forest_param_grid)

    def support_vector_classifier(self) -> None:
        """
        Support Vector Classifier parameters are defined here
        """
        support_vector_param_grid = {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'degree': [2, 3, 4],
            'gamma': ['scale', 'auto'],
            'coef0': [0.0, 1.0, 2.0],
            'shrinking': [True, False],
            'probability': [True, False]
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, support_vector_param_grid)

    def xgboost_classifier(self) -> None:
        """
        XGBoost Classifier parameters are defined here
        """
        xgboost_param_grid = {
            'max_depth': [3, 5, 10],
            'learning_rate': [0.01, 0.1, 1],
            'n_estimators': [10, 50, 100],
            'gamma': [0, 0.1, 0.5],
            'subsample': [0.5, 0.8, 1],
            'colsample_bytree': [0.5, 0.8, 1],
            'reg_alpha': [0, 0.1, 0.5],
            'reg_lambda': [0, 0.1, 0.5]
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, xgboost_param_grid)

    def kernel_ridge_classifier(self) -> None:
        """
        Kernel Ridge Classifier parameters are defined here
        """
        kernel_ridge_param_grid = {
            'alpha': [0.1, 1, 10],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'degree': [2, 3, 4],
            'coef0': [0.0, 1.0, 2.0]
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, kernel_ridge_param_grid)

    def light_gradient_classifier(self) -> None:
        """
        Light Gradient Boosting Classifier parameters are defined here
        """
        light_gradient_param_grid = {
            'boosting_type': ['gbdt', 'dart'],
            'num_leaves': [31, 62, 127],
            'learning_rate': [0.01, 0.1, 1],
            'n_estimators': [10, 50, 100],
            'max_depth': [3, 5, 10],
            'min_data_in_leaf': [10, 50, 100],
            'min_sum_hessian_in_leaf': [0.001, 0.01, 0.1],
            'lambda_l1': [0, 0.1, 0.5],
            'lambda_l2': [0, 0.1, 0.5],
            'feature_fraction': [0.5, 0.8, 1],
            'bagging_fraction': [0.5, 0.8, 1],
            'bagging_freq': [0, 1, 2],
            'early_stopping_round': [5, 10, 20]
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, light_gradient_param_grid)

    def knn_classifier(self) -> None:
        """
        K Nearest Neighbors Classifier parameters are defined here
        """
        knn_param_grid = {
            'n_neighbors': [3, 5, 10],
            'weights': ['uniform', 'distance'],
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
            'leaf_size': [10, 30, 50],
            'p': [1, 2]
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, knn_param_grid)

    def bayesian_linear_classifier(self) -> None:
        """
        Bayesian Linear Classifier parameters are defined here
        """
        bayesian_linear_param_grid = {
            'alpha_1': [0.1, 1, 10],
            'alpha_2': [0.1, 1, 10],
            'lambda_1': [0.1, 1, 10],
            'lambda_2': [0.1, 1, 10],
            'fit_intercept': [True, False]
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, bayesian_linear_param_grid)

    def linear_svc_classifier(self) -> None:
        """
        Linear Support Vector Classifier parameters are defined here
        """
        linear_svc_param_grid = {
            'penalty': ['l1', 'l2'],
            'loss': ['hinge', 'squared_hinge'],
            'dual': [True, False],
            'tol': [0.0001, 0.001, 0.01],
            'C': [0.1, 1, 10],
            'multi_class': ['ovr', 'crammer_singer']
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, linear_svc_param_grid)

    def logistic_regression_classifier(self) -> None:
        """
        Logistic Regression Classifier parameters are defined here
        """
        logistic_regression_param_grid = {
            'penalty': ['l1', 'l2'],
            'dual': [True, False],
            'tol': [0.0001, 0.001, 0.01],
            'C': [0.1, 1, 10],
            'fit_intercept': [True, False],
            'intercept_scaling': [1, 10, 100],
            'class_weight': ['balanced', None],
            'max_iter': [100, 500, 1000],
            'multi_class': ['auto', 'ovr', 'multinomial', 'multinomial'],
            'solver': ['lbfgs', 'liblinear', 'newton', 'sag', 'saga']
        }
        self.model = RandomizedSearchHP(self.model, self.random_state, self.n_iter, logistic_regression_param_grid)
