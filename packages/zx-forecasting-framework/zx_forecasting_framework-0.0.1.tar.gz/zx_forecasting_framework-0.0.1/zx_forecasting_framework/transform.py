import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.api as smt
import seaborn as sns
# import timeSeriesObject, analyse
from .timeSeriesObject import TimeSeriesObject
from .analyse import Analyse
from scipy.stats import boxcox
from math import exp, log

#################################### Class Definitions ########################

class Transform:
    """
    A class used to represent the transform object
    
    Parameters
    ----------
        tso : timeSeriesObject
            timeSeriesObject
        
    Methods
    ----------
        do_boxcox
            Performs the box-cox transformation on the response variable
            
        inverse_boxcox
            Inverses the box-cox transformation on the response variable
            
        stationarize_y
            Stationarizes the response variable 
            
        stationarize_X
            Stationarizes the exogenous variable matrix
    """
    def __init__(self, tso):
        """
        Parameters
        ----------
            tso : timeSeriesObject
                timeSeriesObject
        """
        # Initializing Attributes
        self.tso = tso
        # Auxilliary Attributes
            # X-y 
        self.X = tso.X
        self.y = tso.y
            # y boxcox transformed
        self.yb = tso.y
        self.y_lambda = None
            # Stationary X-y
        self.Xs = tso.X
        self.ys = tso.y
        self.n_lag = None
        self.lags = {}
        self.y_stationary_history = self.tso.y
        self.y_diff_order = None
        
    def do_boxcox(self, lmbda = None):
        """
        Performs the boxcox transformation on the response variable
        Parameters
        ----------
            lmbda : float
                Lambda parameter for the boxcox transformation
        Returns
        ---------
            list : list 
                Box-cox transformed series
        """
        if lmbda == None:
            yb, self.y_lambda = boxcox(x = self.tso.y.dropna())
        else:
            yb = boxcox(x = self.tso.y.dropna(), 
                        lmbda = lmbda)
            self.y_lambda = lmbda
        self.yb = pd.Series(data = list(yb) + [np.nan]*(len(self.tso.y) - len(yb)), 
                            index = self.tso.y.index)
        return self.yb
    
    def inverse_boxcox(self, series):
        """
        Performs the inverse boxcox transformation on the response variable
        Parameters
        ----------
            series : pd.Series
                The transformed series that needs to be inverse transformed
        Returns
        ---------
            list : list 
                Box-cox transformed series
        """
        if self.y_lambda == 0:
            return pd.Series(data = exp(series), index = series.index)
        else:
            return pd.Series(
                data = np.exp(np.log(self.y_lambda * np.abs(series.values) + 1)/self.y_lambda),
                index = series.index)

    
    def unstationarize_v2(self, series, initial_vals):
        z = series.values
        for initial_val in initial_vals:
            z = initial_val + np.cumsum(z)
            
        pass
    
    def stationarize_y(self,):
        """
        Stationarizing the response variable
        
        Parameters
        ----------
        
        Returns
        ----------
            list : list 
                Stationary response variable                
        """
        series = self.yb
        y = pd.DataFrame(data = series.values, 
                         index = series.index, 
                         columns = ['diff_0'])
        z = y.diff_0
        diff_order = 0
        while smt.adfuller(z.dropna())[1]>0.05:
            diff_order = diff_order + 1
            y['diff_{}'.format(diff_order)] = y['diff_{}'.format(diff_order - 1)].diff(1)
            z = y['diff_{}'.format(diff_order)]
        self.y_stationary_history = y
        self.y_diff_order = diff_order
        self.ys = y['diff_{}'.format(diff_order)]
        self.tso.ys = self.ys
        return self.ys

    def stationarize_X(self,):
        """
        Performs the stationarizing operation on the data matrix 
        
        Parameters
        ----------
        
        Returns
        ----------
            dataframe : pd.DataFrame
                the stationarized data matrix 
        """
        X = self.tso.X
        
        for col in X.columns.tolist():
            diff_order = 0
            while smt.adfuller(X[col].dropna())[1]>0.05:
                diff_order = diff_order + 1
                X[col] = X[col].diff(1)
            X = X.rename(columns = {col:col + '_diff_{}'.format(diff_order)})
        self.Xs = X
        self.tso.Xs = self.Xs
        return self.Xs