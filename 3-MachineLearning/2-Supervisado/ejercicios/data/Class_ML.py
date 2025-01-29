import numpy as np
# import pandas as pd

class LinearRegressionBootcamp():
    def __init__(self,normalized=False):
        self.coeficientes = None
        self.intercepto = None
        self.media = None
        self.desviacion_standar = None
        self.normalized = normalized

    def normalizado_futures(self,X):
        self.media = X.mean(axis=0)
        self.desviacion_standar = X.std(axis=0)
        return (X - self.media) / self.desviacion_standar
    
    def fit(self, df, target:str):
        X = df.drop(columns = target)
        y = df[target].values

        if self.normalized:
            X = self.normalizado_futures(X)

        X = np.c_[np.ones(X.shape[0]),X]

        theta = np.linalg.solve(X.T @ X, X.T @ y)

        self.intercepto = theta[0]
        self.coeficientes = theta[1:]

    def predict(self, df):
        if self.coeficientes is None or self.intercepto is None:
            raise ValueError('El modelo no esta entrenado')

        X = df.values()

        if self.normalized:
            X = (X - self.media) / self.desviacion_standar

        y_pred = self.intercepto + np.dot(X,self.coeficientes)

        return y_pred
    

class RegresionLogisticaBootcamp:
    def __init__(self, learning_rate=0.01,max_it=1000):
        self.learning_rate = learning_rate
        self.max_it = max_it
        self.peso = None
        self.sesgo = None

    def _sigmoide(self,z):
        return 1 / (1 + np.exp(-z))

    def _binary_cross_entropy(self,y_true,y_pred):
        
        epsilon = 1e-15 # log de 0
        y_pred = np.clip(y_pred,epsilon,1-epsilon)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

    def fit(self,df,target):
        X = df.drop(columns = target).values
        y = df[target].values

        n_fil,n_columnas = X.shape
        self.peso = np.zeros(n_columnas)
        self.sesgo = 0

        for i in range(self.max_it):
            modelo_lineal = np.dot(X,self.peso) + self.sesgo

            y_pred = self._sigmoide(modelo_lineal)

            dw = (1/n_fil) * np.dot(X.T, (y_pred - y))

            db = (1/n_fil) * np.sum(y_pred-y)

            self.peso -= self.learning_rate * dw
            self.sesgo -= self.learning_rate * db

            if i % 100 == 0:
                loss = self._binary_cross_entropy(y_pred, y)
                print(f'Iteración: {i}, Loss: {loss}')
    
    def predict_proba(self,df):
        if self.peso is None or self.sesgo is None:
            raise Exception('El modelo no ha sido entrenado.')
        
        modelo_lineal = np.dot(df.values,self.peso) + self.sesgo

        return self._sigmoide(modelo_lineal)

    def predict(self,df,threshold=0.5):
        if self.peso is None or self.sesgo is None:
            raise Exception('El modelo no ha sido entrenado.')
        
        probabilidad = self.predict_proba(df) 
        return(probabilidad >= threshold, 1, 0).astype(int)