import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from statsmodels.tsa.api import SimpleExpSmoothing, Holt, ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
# import timeSeriesObject, analyse, transform, metrics
from .timeSeriesObject import TimeSeriesObject
from .analyse import Analyse
from .transform import Transform
from .metrics import Metrics
# import metrics

###############################  Class Definition  ############################

class Model:
    """
    A class used to represent time-series forecating models 
    
    Parameters
    --------
        tso : timeSeriesObject
            timeSeriesObject
        
        tst : transform
            time series transformation object
            
    Methods
    --------
        naive
            Naive forecasting y_t <-- y_{t-1}
        
        seasonal_naive
            Seasonal naive forecasting y_t <-- y_{t-n}
            
        moving_average
            Moving average forecasting with growth factor
            
        simple_exp_smooth
            Simple Exponetial Smoothing forecasting
            
        holt
            Holt Exponential Smoothing forecasting
        
        holt_winters
            Holt-Winters Exponential Smoothing forecasting
            
        linear_regression
            Linear Regression forecasting
            
        elastic_net
            Elastic Net Regression forecasting
            
        random_forest
            Random Forest Regression forecasting
            
        xgboost
            XGBoost Regression forecasting
            
        light_gbm 
            Light GBM Regression forecasting
            
        sarimax
            SARIMAX forecasting
    """
    def __init__(self, tso, tst):
        """
        Parameters
        --------
        tso : timeSeriesObject
            timeSeriesObject
        
        tst : transform
            time series transformation object
        """
        self.tso = tso # time-series object
        self.tst = tst # transformation object
        
        # Auxilliary variables
            # Each Model
        self.mape_list = []
        self.smape_list = []
        self.predictions_list = []
        self.model_list = []
            # Summary Table
        self.summary_table = []
            # Best Model
        self.best_mape = None
        self.best_smape = None
        self.best_predictions = None
        self.best_model = None
    
    def naive(self,):
        """
        Naive forecasting model. The forecast tomorrow is the same as the forecast today
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period 
        """
        # Fitting
        y_test_pred_sb = pd.Series(data = [self.tso.y_train[-1]]*len(self.tso.y_test),
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 

        # Fitting to Train + Test
        y_pred_sb = pd.Series(data = [self.tso.y_test[-1]]*len(self.tso.X_pred),
                                   index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Naive')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Naive')

        return y_test_pred, y_test, y_pred

    def seasonal_naive(self,seasonal_period = 52):
        """
        Seasonal Naive Forecasting Model. The forecast tomorrow is the same as the same day the year before
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        # Fitting
        y_test_pred_sb = pd.Series(data = self.tso.y_train.values[-seasonal_period:-seasonal_period + len(self.tso.X_test)],
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 

        # Fitting to Train + Test
        y_pred_sb = pd.Series(data = pd.concat([self.tso.y_train, self.tso.y_test]).values[-seasonal_period:-seasonal_period + len(self.tso.X_pred)],
                                   index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Seasonal Naive')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Seasonal Naive')

        return y_test_pred, y_test, y_pred
        
        
    def elastic_net(self, alpha = 0.5):
        """
        Linear Regression with L1 and L2 regularization 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        # Model Initialization
        elastic_net_model = ElasticNet(alpha = 0.5)
        # Fitting to Train
        elastic_net_model.fit(self.tso.X_train[3:], self.tso.y_train[3:])
        y_test_pred_sb = elastic_net_model.predict(self.tso.X_test)
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 
        
        # Fitting to Train and Test
        elastic_net_model.fit(pd.concat([self.tso.X_train[3:], self.tso.X_test]), 
                              pd.concat([self.tso.y_train[3:], self.tso.y_test]))
        y_pred_sb = elastic_net_model.predict(self.tso.X_pred)
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Elastic Net')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Elastic-Net')

        return y_test_pred, y_test, y_pred
    
    def linear_regression(self, ):
        """
        Linear Regression with Ordinary Least Squares 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        # Model Initialization
        linreg_model = LinearRegression()
        # Fitting to Train
        linreg_model.fit(self.tso.X_train[3:], self.tso.y_train[3:])
        y_test_pred_sb = linreg_model.predict(self.tso.X_test)
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b)
        # print(y_test_pred, y_test_pred_b)
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 
        
        # Fitting to Train and Test
        linreg_model.fit(pd.concat([self.tso.X_train[3:], self.tso.X_test]), 
                              pd.concat([self.tso.y_train[3:], self.tso.y_test]))
        y_pred_sb = linreg_model.predict(self.tso.X_pred)
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Linear Regression')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Linear Regression')

        return y_test_pred, y_test, y_pred 
    
    def random_forest(self,):
        """
        Scikit-learn implementation of random-forest
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        # Model Initialization
        rf_model = RandomForestRegressor()
        # Fitting to Train
        rf_model.fit(self.tso.X_train[3:], self.tso.y_train[3:])
        y_test_pred_sb = rf_model.predict(self.tso.X_test)
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 
        
        # Fitting to Train and Test
        rf_model.fit(pd.concat([self.tso.X_train[3:], self.tso.X_test]), 
                              pd.concat([self.tso.y_train[3:], self.tso.y_test]))
        y_pred_sb = rf_model.predict(self.tso.X_pred)
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Random Forest')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Random Forest')
        
        return y_test_pred, y_test, y_pred    

    def xgboost(self,):
        """
        eXtreme Gradient Boosting on Decision Trees 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        # Model Initialization
        xgb_model = XGBRegressor()
        # Fitting to Train
        xgb_model.fit(self.tso.X_train[3:], self.tso.y_train[3:])
        y_test_pred_sb = xgb_model.predict(self.tso.X_test)
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 
        
        # Fitting to Train and Test
        xgb_model.fit(pd.concat([self.tso.X_train[3:], self.tso.X_test]), 
                              pd.concat([self.tso.y_train[3:], self.tso.y_test]))
        y_pred_sb = xgb_model.predict(self.tso.X_pred)
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for XGBoost')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('XGBoost')

        return y_test_pred, y_test, y_pred
    
    def light_gbm(self,):
        """
        LightGBM on Decision Trees 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        # Model Initialization
        lgbm_model = LGBMRegressor()
        # Fitting to Train
        lgbm_model.fit(self.tso.X_train[3:], self.tso.y_train[3:])
        y_test_pred_sb = lgbm_model.predict(self.tso.X_test)
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 
        
        # Fitting to Train and Test
        lgbm_model.fit(pd.concat([self.tso.X_train[3:], self.tso.X_test]), 
                              pd.concat([self.tso.y_train[3:], self.tso.y_test]))
        y_pred_sb = lgbm_model.predict(self.tso.X_pred)
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Light GBM')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Light GBM')

        return y_test_pred, y_test, y_pred    

    def moving_average(self, seasonal_period = 26, 
                       window_size = 2, 
                       growth_factor = False):
        """
        Moving Average with growth factor. 
        The prediction tomorrow is a moving average of the actuals in the near history
        and the actuals of the previous season
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        y_test_pred_sb = np.zeros(shape=len(self.tso.y_test))
        if growth_factor:
            for i in range(len(y_test_pred_sb)):
                y_test_pred_sb[i] = np.mean(
                                self.tso.y_train.values[-seasonal_period + i - window_size - 1: -seasonal_period + i - 1])
        else:
            num = np.zeros(shape = len(self.tso.y_test))
            den = np.zeros(shape = len(self.tso.y_test))
            for i in range(len(y_test_pred_sb)):
                num[i] = np.mean(self.tso.y_train.values[-seasonal_period + i - window_size - 1: -seasonal_period + i - 1])
                den[i] = np.mean(self.tso.y_train.values[-2*seasonal_period + i - window_size - 1: -2*seasonal_period + i - 1])
                y_test_pred_sb[i] = (num[i]/den[i]) * self.tso.y_train.values[-seasonal_period + i -window_size]

        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index=self.tso.y_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b) 
        # Fitting to Train + Test
        y_pred_sb = np.zeros(shape=len(self.tso.X_pred))
        if growth_factor:
            for i in range(len(y_pred_sb)):
                y_pred_sb[i] = np.mean(
                                pd.concat([self.tso.y_train, self.tso.y_test]).values[-seasonal_period + i - window_size - 1: -seasonal_period + i - 1])
        else:
            num = np.zeros(shape = len(self.tso.X_pred))
            den = np.zeros(shape = len(self.tso.X_pred))
            for i in range(len(y_pred_sb)):
                num[i] = np.mean(pd.concat([self.tso.y_train, self.tso.y_test]).values[-seasonal_period + i - window_size - 1: -seasonal_period + i - 1])
                den[i] = np.mean(pd.concat([self.tso.y_train, self.tso.y_test]).values[-2*seasonal_period + i - window_size - 1: -2*seasonal_period + i - 1])
                y_pred_sb[i] = (num[i]/den[i]) * pd.concat([self.tso.y_train, self.tso.y_test]).values[-seasonal_period + i -window_size]

        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index=self.tso.X_pred.index)        
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Moving Average')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Moving Average')

        return y_test_pred, y_test, y_pred         
                
    def simple_exp_smoothing(self, smoothing_level = 0.3, optimized = False):
        """
        Simple Exponential Smoothing 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        ses_model = SimpleExpSmoothing(self.tso.y_train[self.tst.y_diff_order:]).fit(smoothing_level = smoothing_level, 
                                                             optimized = optimized)
        y_test_pred_sb = ses_model.forecast(len(self.tso.y_test))
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b)
        
        # Fitting Train + Test
        ses_model = SimpleExpSmoothing(pd.concat([self.tso.y_train[self.tst.y_diff_order:], self.tso.y_test])).fit(smoothing_level=smoothing_level,
                                                                                           optimized=optimized)
        y_pred_sb = ses_model.forecast(len(self.tso.X_pred))
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Simple Exponential Smoothing')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Simple Exponential Smoothing')

        return y_test_pred, y_test, y_pred
        
    def holt(self, smoothing_level = 0.3, smoothing_slope = 0.2, optimized = False):
        """
        Holt's Double Exponential Smoothing Model 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        holt_model = Holt(self.tso.y_train[self.tst.y_diff_order:],
                          exponential = False,
                          damped = False).fit(smoothing_level = smoothing_level,
                                              smoothing_slope = smoothing_slope,
                                              optimized = optimized)
        y_test_pred_sb = holt_model.forecast(len(self.tso.y_test))
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b)
        
        # Fitting Train + Test
        holt_model = Holt(pd.concat([self.tso.y_train[self.tst.y_diff_order:], self.tso.y_test]),
                          exponential = False,
                          damped = False).fit(smoothing_level = smoothing_level,
                                              smoothing_slope = smoothing_slope,
                                              optimized = optimized)
        y_pred_sb = holt_model.forecast(len(self.tso.X_pred))
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Holt Exponential Smoothing')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Holt Exponential Smoothing')

        return y_test_pred, y_test, y_pred
    
    def holt_winters(self, seasonal = 'add', 
                     seasonal_periods = 52, 
                     smoothing_level = 0.3,
                     smoothing_slope = 0.1,
                     smoothing_seasonal = 0.2):
        """
        Holt-Winter Triple Exponential Smoothing 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        holt_model = ExponentialSmoothing(self.tso.y_train[self.tst.y_diff_order:],
                                          seasonal = seasonal,
                                          seasonal_periods = seasonal_periods).fit(smoothing_level = smoothing_level,
                                                                                   smoothing_slope = smoothing_slope,
                                                                                   smoothing_seasonal = smoothing_seasonal)
        y_test_pred_sb = holt_model.forecast(len(self.tso.y_test))
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                   index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b)
        
        # Fitting Train + Test
        holt_model = ExponentialSmoothing(pd.concat([self.tso.y_train[self.tst.y_diff_order:], self.tso.y_test]),
                                          seasonal = seasonal,
                                          seasonal_periods = seasonal_periods).fit(smoothing_level = smoothing_level,
                                                                                   smoothing_slope = smoothing_slope,
                                                                                   smoothing_seasonal = smoothing_seasonal)                                             
        y_pred_sb = holt_model.forecast(len(self.tso.X_pred))
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for Holt-Winters Exponential Smoothing')
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('Holt-Winters Exponential Smoothing')

        return y_test_pred, y_test, y_pred    
    
    def sarimax(self, seasonalities = [26,52]):
        """
        Seasonal Autoregressive Integrated Moving Average with eXogenous variables
        Automatically selects best parameters based on AIC values 
        
        Returns
        --------
        y_test_pred : pd.Series
            Predictions on the test dataset
            
        y_test : pd.Series 
            Actuals of the test dataset
            
        y_pred : pd.Series 
            Predictions for the forecast period
        """
        # Fitting Train
        # return self.tso.X_train
        aic_dict = {}
        for p in range(3):
            for q in range(3):
                for m in seasonalities:                        
                    model = SARIMAX(endog = self.tso.y_train[2:], 
                                    exog = self.tso.X_train[2:], 
                                    order = (p,0,q), 
                                    seasonal_order=(0,0,0,m)).fit(disp = 0)
                    aic_dict[str(p)+ '-' + str(q) + '-' + str(m)] = model.aic
        aic_table = pd.DataFrame(aic_dict.values(), index = aic_dict.keys()).rename(columns={0: 'aic'})
        optimal_vals = aic_table[aic_table.aic == aic_table.aic.min()].index[-1].split("-")
        p,q,m = int(optimal_vals[0]), int(optimal_vals[1]), int(optimal_vals[2])        
        model = SARIMAX(endog = self.tso.y_train[2:], 
                        exog = self.tso.X_train[2:], 
                        order = (p,0,q), 
                        seasonal_order=(0,0,0,m)).fit()
        y_test_pred_sb = model.forecast(len(self.tso.y_test), 
                                        exog = self.tso.X_test)
        y_test_pred_sb = pd.Series(data = y_test_pred_sb, 
                                    index = self.tso.X_test.index)
        y_test_sb = self.tso.y_test
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order > 0:
            y_test_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] +\
                np.cumsum(y_test_pred_sb)
            y_test_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) - 1] + \
                np.cumsum(y_test_sb)            
            diff_order = diff_order - 1
        y_test_pred_b = y_test_pred_sb
        y_test_b = y_test_sb
        # Inverse-Boxcox
            # Testing Predictions
        y_test_pred = self.tst.inverse_boxcox(y_test_pred_b) 
            # Testing Actuals
        y_test = self.tst.inverse_boxcox(y_test_b)
        
        # Fitting Train + Test
        model = SARIMAX(endog = pd.concat([self.tso.y_train[2:], self.tso.y_test]), exog = pd.concat([self.tso.X_train[2:],self.tso.X_test]), 
                        order = (p,0,q), 
                        seasonal_order=(0,0,0,m)).fit()
        y_pred_sb = model.forecast(len(self.tso.X_pred), 
                                   exog = self.tso.X_pred)
        y_pred_sb = pd.Series(data = y_pred_sb, 
                              index = self.tso.X_pred.index)
        # Destationarizing
        diff_order = self.tst.y_diff_order
        y_stationary_history = self.tst.y_stationary_history
        while diff_order>0:
            y_pred_sb = y_stationary_history['diff_{}'.format(diff_order - 1)].iloc[len(self.tso.y_train) + len(self.tso.y_test) - 1] + \
                        np.cumsum(y_pred_sb)
            diff_order = diff_order - 1
        y_pred_b = y_pred_sb
        # Inverse-Boxcox
            # Predictions
        y_pred = self.tst.inverse_boxcox(y_pred_b)
        
        # Visualize
        plt.figure(figsize = (14,6))
        plt.plot(self.tst.y, label = 'Historical')
        plt.plot(y_test, label = 'Actuals')
        plt.plot(y_test_pred, label = 'Forecast')
        plt.plot(y_pred, label = 'Predictions')
        plt.title('Forecast vs Actuals and Predictions for SARIMAX({},{},{},{})'.format(p,0,q,m))
        plt.legend()
        plt.show()
        
        # Evaluate
        smape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).smape
        mape = metrics.Metrics(y_true = y_test, y_predicted = y_test_pred).mape
    
        # Update list
        self.smape_list.append(smape)
        self.mape_list.append(mape)
        self.predictions_list.append(y_pred.values.tolist())
        self.model_list.append('SARIMAX')

        return y_test_pred, y_test, y_pred  

    def construct_summary_table(self,):
        """
        Constructs and returns summary table 
        
        Returns
        -------
        summary_table : pd.DataFrame 
            Summary Table containing Model Name, MAPE, SMAPE, Predictions
        """
        self.naive()
        self.seasonal_naive()
        self.moving_average()
        self.linear_regression()
        self.elastic_net()
        self.random_forest()
        self.xgboost()
        self.light_gbm()
        self.simple_exp_smoothing()
        self.holt()
        self.holt_winters()
        self.sarimax()
        self.summary_table = pd.DataFrame(data = {'model_name':self.model_list,
                                                  'smape':self.smape_list,
                                                  'mape':self.mape_list,
                                                  'predictions':self.predictions_list},
                                          index = [i+1 for i in range(len(self.model_list))])
        return self.summary_table
    
    def find_best_model(self, criteria = 'mape',):
        """
        Finds the best model of all the models run
        
        Returns
        -------
        best_model_stats : pd.DataFrame
            Best model name, MAPE, SMAPE, Predictions
        """
        if type(self.summary_table) == pd.DataFrame:
            summary_table = self.summary_table
        else:
            summary_table = self.construct_summary_table()
        min_metric = summary_table[criteria].min()
        best_model_stats = summary_table[summary_table[criteria] == min_metric]
        self.best_mape = best_model_stats.mape.values[0]
        self.best_model = best_model_stats.model_name.values[0]
        self.best_predictions = pd.Series(data = best_model_stats.predictions.values[0],
                                          index = self.tso.X_pred.index)
        self.best_smape = best_model_stats.smape.values[0]

        return best_model_stats