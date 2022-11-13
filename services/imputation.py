import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from autoimpute.imputations import SingleImputer
from my_utils.enums import ImputationStatus, SimpleImputationMethods, InterpolationImputationMethods, OtherImputationMethods
from database.models import TimeSerie as TimeSerieModel
from uuid import uuid4
from time import sleep

def simple_imputation(data: list[float], method: str = 'mean', job_hash: str = '') -> list[float]:
  '''
  Performs mean, median or most_common imputation to an univariate time series.

  Args:
    data (list of float): The time series to be imputed with mean imputation
    method (str): Method to be used in the imputation
  
  Returns:
    list of float: The resulting time series after imputation
  '''

  TimeSerieModel().set_status(job_hash, ImputationStatus.PROCESSING)

  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  simple_imputer = SimpleImputer(missing_values=np.nan, strategy=method)
  imputed_data = simple_imputer.fit_transform(data_np)

  imputed_series = imputed_data.reshape((-1)).tolist() # reshape back to 1d array and parse to a python list

  TimeSerieModel().finish_imputation(job_hash, imputed_series)

  return

def imputation_by_interpolation(data: list[float], method: str = 'linear', job_hash: str = '') -> list[float]:
  '''
    Performs imputation by interpolation to an univariate time series.

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used in the imputation by interpolation
    
    Returns:
      list of float: The resulting time series after imputation
  '''

  timeSerieModel = TimeSerieModel()

  timeSerieModel.set_status(job_hash, ImputationStatus.PROCESSING)

  order = None
  if 'spline' in method or 'polynomial' in method:
    [order, method] = map(lambda el: el.strip(), method.split('-order'))
    order = int(order)
  
  try: 
    data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

    data_df = pd.DataFrame(data_np)

    single_imputer = SingleImputer(
      strategy='interpolate',
      imp_kwgs={'interpolate': {'fill_strategy': method, 'order': order}}
    )

    imputed_data_df = single_imputer.fit_transform(data_df)

    imputed_series = imputed_data_df[0].tolist()

    timeSerieModel.finish_imputation(job_hash, imputed_series)
  except Exception as e:
    timeSerieModel.set_error(job_hash, str(e))
  return

def imputation_by_other_methods(data: list[float], method: str = 'mode', job_hash: str = ''):
  '''
    Performs imputation using Autoimpute SingleImputer and the given method

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used 
    
    Returns:
      list of float: The resulting time series after imputation
  '''

  TimeSerieModel().set_status(job_hash, ImputationStatus.PROCESSING)
  
  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  data_df = pd.DataFrame(data_np)

  single_imputer = SingleImputer(strategy=method)

  imputed_data_df = single_imputer.fit_transform(data_df)

  imputed_series = imputed_data_df[0].tolist()

  TimeSerieModel().finish_imputation(job_hash, imputed_series)

  return

def create_imputation(data: list[float], method: str, job_hash: str) -> str:

  simple_methods = [member.value for member in SimpleImputationMethods]
  interpolation_methods = [member.value for member in InterpolationImputationMethods]
  other_methods = [member.value for member in OtherImputationMethods]

  if method in simple_methods:
    method = 'most_frequent' if method == 'most frequent' else method

    simple_imputation(data, method, job_hash)

  elif method in interpolation_methods:
    interpolation_strategy = method.replace('interpolation', '').strip()

    imputation_by_interpolation(data, interpolation_strategy, job_hash)
  
  elif method in other_methods:
    imputation_by_other_methods(data, method, job_hash)
  
  else:
    TimeSerieModel().set_error(job_hash, 'no method found')

  return

  
