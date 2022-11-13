import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from autoimpute.imputations import SingleImputer
from my_utils.enums import ImputationStatus
from database.models import TimeSerie as TimeSerieModel
from uuid import uuid4
import asyncio

async def simple_imputation(data: list[float], method: str = 'mean', job_hash: str = '') -> list[float]:
  print('SIMPLE IMPUTATION')

  '''
  Performs mean, median or most_common imputation to an univariate time series.

  Args:
    data (list of float): The time series to be imputed with mean imputation
    method (str): Method to be used in the imputation
  
  Returns:
    list of float: The resulting time series after imputation
  '''

  await asyncio.sleep(30)
  print('SET STATUS')


  TimeSerieModel().set_status(job_hash, ImputationStatus.PROCESSING)

  await asyncio.sleep(30)

  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  simple_imputer = SimpleImputer(missing_values=np.nan, strategy=method)
  imputed_data = simple_imputer.fit_transform(data_np)

  imputed_series = imputed_data.reshape((-1)).tolist() # reshape back to 1d array and parse to a python list

  print('FINISH IMPUTATION')

  TimeSerieModel().finish_imputation(job_hash, imputed_series)

  return

async def imputation_by_interpolation(data: list[float], method: str = 'linear', job_hash: str = '') -> list[float]:
  '''
    Performs imputation by interpolation to an univariate time series.

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used in the imputation by interpolation
    
    Returns:
      list of float: The resulting time series after imputation
  '''
  await asyncio.sleep(30)

  TimeSerieModel().set_status(ImputationStatus.PROCESSING)

  await asyncio.sleep(30)
  
  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  data_df = pd.DataFrame(data_np)

  single_imputer = SingleImputer(
    strategy='interpolate',
    imp_kwgs={'interpolate': {'fill_strategy': method}}
  )

  imputed_data_df = single_imputer.fit_transform(data_df)

  imputed_series = imputed_data_df[0].tolist()

  TimeSerieModel().finish_imputation(job_hash, imputed_series)

  return

async def imputation_by_other_methods(data: list[float], method: str = 'mode', job_hash: str = ''):
  '''
    Performs imputation using Autoimpute SingleImputer and the given method

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used 
    
    Returns:
      list of float: The resulting time series after imputation
  '''
  await asyncio.sleep(30)

  TimeSerieModel().set_status(ImputationStatus.PROCESSING)

  await asyncio.sleep(30)
  
  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  data_df = pd.DataFrame(data_np)

  single_imputer = SingleImputer(strategy=method)

  imputed_data_df = single_imputer.fit_transform(data_df)

  imputed_series = imputed_data_df[0].tolist()

  TimeSerieModel().finish_imputation(job_hash, imputed_series)

  return

def create_imputation(data: list[float], method: str, job_hash: str) -> str:
  print('CREATE IMPUTATION')
  return
  if method in ['mean', 'median', 'most frequent']:
    method = 'most_frequent' if method == 'most frequent' else method
    simple_imputation(data, method, job_hash)

  elif method in ['linear interpolation', 'time interpolation', 'quadratic interpolation',
    'cubic interpolation', 'spline interpolation', 'barycentric interpolation',
    'polynomial interpolation']:

    interpolation_strategy = method.replace('interpolation', '').strip()

    imputation_by_interpolation(data, interpolation_strategy, job_hash)
  
  elif method in ['mode', 'random', 'locf', 'nocb', 'normal unit variance']:
    imputation_by_other_methods(data, method, job_hash)

  return

  
