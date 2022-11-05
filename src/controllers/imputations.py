import numpy as np
from sklearn.impute import SimpleImputer

def simple_imputation(time_series: list[float], method: str = 'mean') -> list[float]:
  '''
  Performs simple statistic imputation to a univariate time series.

  Args:
    time_series (list of float): The time series to be imputed with mean imputation
    method (str): Method to be used in the imputation
  
  Returns:
    list of float: The resulting time series after mean imputation
  '''

  mean_imputer = SimpleImputer(missing_values=np.nan, strategy=method)
  my_time_series = np.array(time_series, dtype=np.float).reshape((-1, 1)) # reshape to 2d array
  imputed_data = mean_imputer.fit_transform(my_time_series)

  return imputed_data.reshape((-1)).tolist() # reshape back to 1d array and parse to a python list