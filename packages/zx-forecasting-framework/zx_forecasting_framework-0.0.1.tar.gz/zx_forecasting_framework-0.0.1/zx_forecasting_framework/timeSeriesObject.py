import pandas as pd
import numpy as np

#################################### Class Definitions ########################

class TimeSeriesObject:
    """
    A class that defines the time-series object 
    
    Attributes: 
        df : pd.DataFrame
            The dataframe containing the time-series data
        
        response_variable : str
            Column name containing the response variable 
            
        date_columns : str 
            Column name containing the date column 
            
        drop_col : str 
            Columns name which needs to be dropped, must be part of original dataframe 
            
        add_col : str 
            Column name which needs to be added, must be part of original dataframe   
            
        start_train_date : pd.datetime
            Date from which training is to be started 
            
        end_train_date : pd.datetime
            Date till which training is to be done 
            
        start_test_date : pd.datetime 
            Date from which testing is to be started 
            
        end_test_date : pd.datetime 
            Date till which testning is to be done
            
        start_pred_date : pd.datetime
            Date from which prediction is to be started 
             
        end_pred_date : pd.datetime 
            Date till which prediction is to be done  
    """
    
    def __init__(self, df):
        """
        Parameters
        ----------
        df : pd.DataFrame
            The dataframe containing the time series data
        """
        # Instantiating variables
        self.df = df
        
        # Auxilliary variables
            # target 
        self.response_variable = None
            # modified df
        self.dfm = df
            # date column
        self.date_column = None
            # X-y splits
        self.X = None
        self.y = None
            # Stationary X-y
        self.Xs = self.X
        self.ys = self.y
            # feature selection
        self.Xsf = None
        self._selected_features = []
            
            # train-test-pred splits
        self.X_train = None
        self.X_test = None
        self.X_pred = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
    
    def set_date_column(self, date_column):
        """
        Parameters
        ----------
        date_column : str
            Column name containing the date column
            
        Returns
        ----------
        self : timeSeriesObject
            timeSeriesObject
        """
        self.df = self.df.set_index(date_column)
        self.df.index = pd.to_datetime(self.df.index, format = '%d-%m-%Y')
        self.dfm = self.df
        return self
    
    def drop_col(self, drop_col):
        """
        Parameters
        ----------
        drop_col : str
            Columns name that is to be dropped
        Returns
        ----------
        self : timeSeriesObject
            timeSeriesObject
        """
        self.dfm = self.dfm.drop(drop_col, axis = 1)
        return self
    
    def add_col(self, add_col):
        """
        Parameters
        ----------
        add_col : str
            Columns name that is to be dropped
        Returns
        ----------
        self : timeSeriesObject
            timeSeriesObject
        """
        col_list = self.dfm.columns.tolist() + [add_col] 
        self.dfm = self.df[col_list]
        return self
    
    def xy_split(self, response_variable):
        """
        Parameters
        ----------
        response_variable : str
            Columns name that is the response variable
        Returns
        ----------
        self : timeSeriesObject
            timeSeriesObject
        """
        self.response_variable = response_variable
        self.y = self.dfm[response_variable]
        self.X = self.dfm.drop(response_variable, axis = 1)
        self.Xm = self.X
        self.Xs = self.X
        self.ys = self.y
        return self
        
    def train_test_split(self, 
                         start_train_date,
                         end_train_date,
                         start_test_date,
                         end_test_date,
                         start_pred_date,
                         end_pred_date):
        """
        Parameters
        ----------
                start_train_date : pd.datetime
            Date from which training is to be started 
            
        end_train_date : pd.datetime
            Date till which training is to be done 
            
        start_test_date : pd.datetime 
            Date from which testing is to be started 
            
        end_test_date : pd.datetime 
            Date till which testning is to be done
            
        start_pred_date : pd.datetime
            Date from which prediction is to be started 
             
        end_pred_date : pd.datetime 
            Date till which prediction is to be done  
        Returns
        ----------
        self : timeSeriesObject
            timeSeriesObject
        """
        self.X_train = self.Xs.loc[start_train_date:end_train_date]
        self.y_train = self.ys.loc[start_train_date:end_train_date]
        self.X_test = self.Xs.loc[start_test_date:end_test_date]
        self.y_test = self.ys.loc[start_test_date:end_test_date]
        self.X_pred = self.Xs.loc[start_pred_date:end_pred_date]
        self.y_pred = np.nan * len(self.X_pred)
        return self