import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from autoimpute.imputations import SingleImputer
from my_utils.enums import ImputationStatus
from database.models import TimeSerie as TimeSerieModel

def simple_imputation(data: list[float], method: str = 'mean') -> list[float]:
  '''
  Performs mean, median or most_common imputation to an univariate time series.

  Args:
    data (list of float): The time series to be imputed with mean imputation
    method (str): Method to be used in the imputation
  
  Returns:
    list of float: The resulting time series after imputation
  '''

  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  simple_imputer = SimpleImputer(missing_values=np.nan, strategy=method)
  imputed_data = simple_imputer.fit_transform(data_np)

  return imputed_data.reshape((-1)).tolist() # reshape back to 1d array and parse to a python list

def imputation_by_interpolation(data: list[float], method: str = 'linear') -> list[float]:
  '''
    Performs imputation by interpolation to an univariate time series.

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used in the imputation by interpolation
    
    Returns:
      list of float: The resulting time series after imputation
  '''
  
  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  data_df = pd.DataFrame(data_np)

  single_imputer = SingleImputer(
    strategy='interpolate',
    imp_kwgs={'interpolate': {'fill_strategy': method}}
  )

  imputed_data_df = single_imputer.fit_transform(data_df)

  return imputed_data_df[0].tolist()

def imputation_by_other_methods(data: list[float], method: str = 'mode'):
  '''
    Performs imputation using Autoimpute SingleImputer and the given method

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used 
    
    Returns:
      list of float: The resulting time series after imputation
  '''
  
  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  data_df = pd.DataFrame(data_np)

  single_imputer = SingleImputer(strategy=method)

  imputed_data_df = single_imputer.fit_transform(data_df)

  return imputed_data_df[0].tolist()


def create_imputation(data: list[float], method: str) -> list[float]:
  if len(data) == 0: 
    return []
  
  imputed_data = []
  
  if method in ['mean', 'median', 'most frequent']:
    method = 'most_frequent' if method == 'most frequent' else method
    imputed_data = simple_imputation(data, method)

  elif method in ['linear interpolation', 'time interpolation', 'quadratic interpolation',
    'cubic interpolation', 'spline interpolation', 'barycentric interpolation',
    'polynomial interpolation']:

    interpolation_strategy = method.replace('interpolation', '').strip()

    imputed_data = imputation_by_interpolation(data, interpolation_strategy)
  
  elif method in ['mode', 'random', 'locf', 'nocb', 'normal unit variance']:
    imputed_data = imputation_by_other_methods(data, method)

  if (imputed_data) == 0:
    return None

  new_imputed_series = {
    'series': imputed_data,
    'status': ImputationStatus.FINISHED.value
  }

  time_serie = TimeSerieModel()
  hash = time_serie.insert(new_imputed_series)

  return hash

  
