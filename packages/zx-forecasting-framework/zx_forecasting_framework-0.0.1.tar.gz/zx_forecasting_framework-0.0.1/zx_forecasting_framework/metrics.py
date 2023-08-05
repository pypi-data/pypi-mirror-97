import numpy as np
import warnings

#######################################  Data  ################################
class Metrics:
    """
    A class used to represent the metrics relevant for time-series 
    
    Attributes
    ----------
    y_true : pd.Series
        The actuals 
    y_predicted : pd.Series
        The forecasts
    
    Methods
    ----------
    coef_variation 
        Coefficient of Variation
        
    avg_demand_interval
        Average Demand Interval
        
    mean_absolute_error
        MAE
        
    mean_absolute_percentage_error
        MAPE
        
    symmetric_mean_absolute_percentage_error
        SMAPE
    """
    
    def __init__(self, y_true, y_predicted = None):
        """
        Parameters
        ----------
            y_true : pd.Series
                The actuals 
            y_predicted : pd.Series
                The forecasts
        """
        # Instantiation Attributes
        self.y_true = np.ravel(np.array(y_true))
        if (y_predicted is not None):
            self.y_predicted = np.ravel(np.array(y_predicted))

        # Metrics
        self.cov = np.round(self.coef_variation(), 2)
        self.adi = np.round(self.avg_demand_interval(), 2)
        if (y_predicted is not None):
            self.mae = np.round(self.mean_absolute_error(), 2)
            self.mape = np.round(self.mean_absolute_percentage_error(), 2)
            self.smape = np.round(self.sym_mean_absolute_percentage_error(), 2)
        else:
            warnings.warn("No 'y_predicted' passed")

    # Univariate Metrics

    def coef_variation(self):
        """
        Coefficient of variation of the response time series
        
        Parameters
        ----------
        
        Returns
        -------
        COV of the actual time series
        """
        return np.std(self.y_true)/np.mean(self.y_true)

    def avg_demand_interval(self):
        """
        Average Demand Interval for the response time series
        
        Parameters
        ----------
        
        Returns
        -------
        ADI of the actual time series
        """
        return len(self.y_true)/sum(self.y_true > 0)

    # Bivariate Metrics

    def mean_absolute_error(self):
        """
        Mean Absolute Error for the predicted time series 
        with respect to the actual time series
        
        Parameters
        ----------
        
        Returns
        -------
        MAE of the forecasted time series with respect to the actuals 
        """
        if len(self.y_predicted) == 0:
            return None
        else:
            return np.mean(np.abs(self.y_true - self.y_predicted))

    def mean_absolute_percentage_error(self):
        """
        Mean Absolute Percentage Error for the predicted time series 
        with respect to the actual time series
        
        Parameters
        ----------
        
        Returns
        -------
        MAPE of the forecasted time series with respect to the actuals
        """
        if len(self.y_predicted) == 0:
            return None
        else:
            return 100 * np.mean(np.abs(self.y_true - self.y_predicted)/ self.y_true)

    def sym_mean_absolute_percentage_error(self):
        """
        Symmetric Mean Absolute Percentage Error for the 
        predicted time series with respect to the actual time series
        
        Parameters
        ----------
        
        Returns
        -------
        SMAPE of the forecasted time series with respect to the actuals
        """
        if len(self.y_predicted) == 0:
            return None
        else:
            return 200 * np.mean(np.abs(self.y_true - self.y_predicted)/ (self.y_true + self.y_predicted))