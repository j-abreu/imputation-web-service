import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from autoimpute.imputations import SingleImputer
from my_utils.enums import ImputationStatus, SimpleImputationMethods, InterpolationImputationMethods, OtherImputationMethods
from database.models import TimeSerie as TimeSerieModel
from uuid import uuid4
from time import sleep

def get_null_values_indexes(data: list[float]) -> list[int]:
  data_df = pd.DataFrame(data)
  
  return data_df[data_df[0].isnull()].index.tolist()

def simple_imputation(data: list[float], method: str = 'mean', job_id: str = '') -> list[float]:
  '''
  Performs mean, median or most_common imputation to an univariate time series.

  Args:
    data (list of float): The time series to be imputed with mean imputation
    method (str): Method to be used in the imputation
  
  Returns:
    list of float: The resulting time series after imputation
  '''

  TimeSerieModel().set_status(job_id, ImputationStatus.PROCESSING)

  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  simple_imputer = SimpleImputer(missing_values=np.nan, strategy=method)
  imputed_data = simple_imputer.fit_transform(data_np)

  imputed_series = imputed_data.reshape((-1)).tolist() # reshape back to 1d array and parse to a python list

  TimeSerieModel().finish_imputation(job_id, imputed_series)

  return

def imputation_by_interpolation(data: list[float], method: str = 'linear', order: int = None, job_id: str = '') -> list[float]:
  '''
    Performs imputation by interpolation to an univariate time series.

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used in the imputation by interpolation
      order: Order for polynomial or spline method
      job_id: Unique identifier for the job
    
    Returns:
      list of float: The resulting time series after imputation
  '''

  timeSerieModel = TimeSerieModel()

  timeSerieModel.set_status(job_id, ImputationStatus.PROCESSING)
  
  try: 
    data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

    data_df = pd.DataFrame(data_np)

    single_imputer = SingleImputer(
      strategy='interpolate',
      imp_kwgs={'interpolate': {'fill_strategy': method, 'order': order}}
    )

    imputed_data_df = single_imputer.fit_transform(data_df)

    imputed_series = imputed_data_df[0].tolist()

    timeSerieModel.finish_imputation(job_id, imputed_series)
  except Exception as e:
    timeSerieModel.set_error(job_id, str(e))
  return

def imputation_by_other_methods(data: list[float], method: str = 'mode', job_id: str = ''):
  '''
    Performs imputation using Autoimpute SingleImputer and the given method

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used
      job_id: Unique identifier for the job
    
    Returns:
      list of float: The resulting time series after imputation
  '''

  TimeSerieModel().set_status(job_id, ImputationStatus.PROCESSING)
  
  data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

  data_df = pd.DataFrame(data_np)

  single_imputer = SingleImputer(strategy=method)

  imputed_data_df = single_imputer.fit_transform(data_df)

  imputed_series = imputed_data_df[0].tolist()

  TimeSerieModel().finish_imputation(job_id, imputed_series)

  return

def create_imputation(data: list[float], method: dict[str, str], job_id: str) -> str:

  method_name = method['name']
  method_order = method['order']

  print(method_name, method_order)

  time_series = TimeSerieModel()

  time_series.update_by_id(job_id, {
    'status': ImputationStatus.PROCESSING.value,
    'imputed_indexes': get_null_values_indexes(data)
  })

  simple_methods = [member.value for member in SimpleImputationMethods]
  interpolation_methods = [member.value for member in InterpolationImputationMethods]
  other_methods = [member.value for member in OtherImputationMethods]

  if method_name in simple_methods:
    method_name = 'most_frequent' if method_name == 'most frequent' else method_name

    simple_imputation(data, method_name, job_id)

  elif method_name in interpolation_methods:
    interpolation_strategy = method_name.replace('interpolation', '').strip()

    imputation_by_interpolation(data, interpolation_strategy, method_order, job_id)
  
  elif method_name in other_methods:
    imputation_by_other_methods(data, method_name, job_id)
  
  else:
    TimeSerieModel().set_error(job_id, 'no method found')

  return

  
