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

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

class ClassifierModel:
    def __init__(self, model):
        self.model = model

    def train(self, X, y):
        """Train the model using the given training data."""
        self.model.fit(X, y)

    def predict(self, X):
        """Make predictions using the trained model."""
        return self.model.predict(X)
    
    def evaluate(self, X, y):
        """Calculate and return multiple evaluation metrics."""
        y_pred = self.predict(X)
        accuracy = accuracy_score(y, y_pred)
        f1 = f1_score(y, y_pred, average='weighted')
        precision = precision_score(y, y_pred, average='weighted')
        recall = recall_score(y, y_pred, average='weighted')
        return accuracy, f1, precision, recall


class GradientBoostingClassifierModel(ClassifierModel):
    def __init__(self):
        from sklearn.ensemble import GradientBoostingClassifier
        super().__init__(model=GradientBoostingClassifier())


class RandomForestClassifierModel(ClassifierModel):
    def __init__(self):
        from sklearn.ensemble import RandomForestClassifier
        super().__init__(model=RandomForestClassifier())


class XGBClassifierModel(ClassifierModel):
    def __init__(self):
        from xgboost import XGBClassifier
        super().__init__(model=XGBClassifier())


class LogisticRegressionModel(ClassifierModel):
    def __init__(self):
        from sklearn.linear_model import LogisticRegression
        super().__init__(model=LogisticRegression())


class LightGradientClassifierModel(ClassifierModel):
    def __init__(self):
        from lightgbm import LGBMClassifier
        super().__init__(model=LGBMClassifier())


class SVCModel(ClassifierModel):
    def __init__(self):
        from sklearn.svm import SVC
        super().__init__(model=SVC())


class KNNClassifierModel(ClassifierModel):
    def __init__(self):
        from sklearn.neighbors import KNeighborsClassifier
        super().__init__(model=KNeighborsClassifier())


class DecisionTreeClassifierModel(ClassifierModel):
    def __init__(self):
        from sklearn.tree import DecisionTreeClassifier
        super().__init__(model=DecisionTreeClassifier())


class NaiveBayesClassifierModel(ClassifierModel):
    def __init__(self):
        from sklearn.naive_bayes import GaussianNB
        super().__init__(model=GaussianNB())