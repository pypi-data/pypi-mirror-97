import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.api as smt
import seaborn as sns
from .timeSeriesObject import TimeSeriesObject

#################################### Class Definitions ########################

class Analyse:
    """
    A class used to represent the Analysis functionalities for time-series
    
    Attributes:
        tso: timeSeriesObject
            A timeSeriesObject (to be analysed)
            
    Methods:
        visual_summary
            Provides a visual summary of the time series passed, with it's time series plots, 
            and the ACF and PACF plots
            
        _split(a,n)
            Splits the iterable a into n parts, whilst preserving the ordering
            
        intermittency(n_chunks)
            Plots the COV vs the ADI for each segment of the time series, to visually eaxmine 
            the demand characteristics and classify them into one of the four buckets
    """
    def __init__(self, tso):
        """
        Parameters:
            tso: timeSeriesObject
        """
        # Initializing Attributes
        self.tso = tso
        # Auxilliary Attributes
            # X-y (to be replaced by self.tso.X, self.tso.y)
        self.X = tso.X
        self.y = tso.y
            # Intermittency Measure
        self.adi = None
        self.cov = None
        
    def visual_summary(self, series):
        """
        Prints the time-series plot, the ACF and the PACF of the passed series
        
        Parameters:
            series : pd.Series 
        Returns:
             fig : matplotlib.pyplot.figure
        """
        plt.figure(figsize = (10,10))
        layout = (2,2)
        ts_ax = plt.subplot2grid(layout, (0,0), colspan = 2)
        acf_ax = plt.subplot2grid(layout, (1,0))
        pacf_ax = plt.subplot2grid(layout, (1,1))
        
        
        series.plot(ax = ts_ax, )
        smt.graphics.plot_acf(series, lags=int(len(series)/3), ax=acf_ax)
        smt.graphics.plot_pacf(series, lags=int(len(series)/3), ax=pacf_ax)
        [ax.set_xlim(1.5) for ax in [acf_ax, pacf_ax]]
        sns.despine()
        plt.tight_layout()
        return ts_ax, acf_ax, pacf_ax
    
    def _split(self, a, n):
        """
        Splits a into n nearly equal parts, whilst preserving order 
        
        Parameters:
            a : np.array
                Iterable which needs to be spliced
            n : int
                Number of nearly equal parts in which the array needs to be spliced into
        Returns:
            list : 
                List of n lists, containing the spliced a array 
        """
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

    def intermittency(self, n_chunks = 6):
        """
        Plots COV vs ADI for demand classification
        
        Parameters:
            n_chunks : 
                Number of parts the time-series needs to be split into
        Returns:
            plot : matplotlib.pyplot.figure
        """
        self.cov = np.std(self.y)/np.mean(self.y)
        self.adi = len(self.y)/sum(self.y > 0)
        
        plt.figure(figsize = (6,6))
        i = 0
        for y_chunk in list(self._split(self.y.values, n_chunks)):
            plt.plot((np.std(y_chunk)/np.mean(y_chunk))**2,
                     len(y_chunk)/sum(y_chunk > 0), 
                     marker = 'o', 
                     alpha = ((i+1)/n_chunks),
                     color = 'blue')
            i+=1
        plt.title('COV vs ADI plot for Demand Classification')
        plt.xlabel('COV^2')
        plt.ylabel('ADI')
        plt.xlim([0,1])
        plt.ylim([0,5])
        plt.plot([0.49, 0.49], [0,5], color = 'green')
        plt.plot([0.0, 1.0], [1.32, 1.32], color = 'green')
        plt.annotate('Smooth', xy = (0.2,0.5))
        plt.annotate('Erratic', xy = (0.8, 0.5))
        plt.annotate('Intermittent', xy = (0.2,3))
        plt.annotate('Lumpy', xy = (0.8, 3))
        return plt