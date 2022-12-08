import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from autoimpute.imputations import SingleImputer
from my_utils.enums import ImputationStatus, ImputationMethods, SimpleImputationMethods, InterpolationImputationMethods, OtherImputationMethods
from database.models import ImputationModel
from uuid import uuid4
from time import sleep

def get_null_values_indexes(data: list[float]) -> list[int]:
  data_df = pd.DataFrame(data)
  
  return data_df[data_df[0].isnull()].index.tolist()

def simple_imputation(data: list[float], method: str = 'mean') -> list[float]:
  '''
  Performs mean, median or most_common imputation to an univariate time series.

  Args:
    data (list of float): The time series to be imputed with mean imputation
    method (str): Method to be used in the imputation
  
  Returns:
    list of float: The resulting time series after imputation
  '''

  imputed_data = None
  
  try:
    data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

    simple_imputer = SimpleImputer(missing_values=np.nan, strategy=method)
    imputed_data = simple_imputer.fit_transform(data_np)

    imputed_series = imputed_data.reshape((-1)).tolist() # reshape back to 1d array and parse to a python list

  except Exception as e:
    return str(e)

  return imputed_series

def imputation_by_interpolation(data: list[float], method: str = 'linear', order: int = None) -> list[float] | str:
  '''
    Performs imputation by interpolation to an univariate time series.

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used in the imputation by interpolation
      order: Order for polynomial or spline method
    
    Returns:
      list of float: The resulting time series after imputation
  '''

  imputed_series = None

  try: 
    data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

    data_df = pd.DataFrame(data_np)

    single_imputer = SingleImputer(
      strategy='interpolate',
      imp_kwgs={'interpolate': {'fill_strategy': method, 'order': order}}
    )

    imputed_data_df = single_imputer.fit_transform(data_df)

    imputed_series = imputed_data_df[0].tolist()

  except Exception as e:
    return str(e)
  
  return imputed_series


def imputation_by_other_methods(data: list[float], method: str = 'mode') -> list[float]:
  '''
    Performs imputation using Autoimpute SingleImputer and the given method

    Args:
      data (list of float): The time series to be imputed with mean imputation
      method (str): Method to be used
    
    Returns:
      list of float: The resulting time series after imputation
  '''

  imputed_series = None

  try:
    data_np = np.array(data, dtype=np.float).reshape((-1, 1)) # reshape to 2d array

    data_df = pd.DataFrame(data_np)

    single_imputer = SingleImputer(strategy=method)

    imputed_data_df = single_imputer.fit_transform(data_df)

    imputed_series = imputed_data_df[0].tolist()
  except Exception as e:
    return str(e)

  return imputed_series


def route(data: list[float], method_name: str, method_order: int) -> list[float]:
  simple_methods = [member.value for member in SimpleImputationMethods]
  interpolation_methods = [member.value for member in InterpolationImputationMethods]
  other_methods = [member.value for member in OtherImputationMethods]

  imputation_results = []

  if method_name in simple_methods:
    method_name = 'most_frequent' if method_name == 'most frequent' else method_name

    imputation_results = simple_imputation(data, method_name)

  elif method_name in interpolation_methods:
    interpolation_strategy = method_name.replace('interpolation', '').strip()

    imputation_results = imputation_by_interpolation(data, interpolation_strategy, method_order)
  
  elif method_name in other_methods:
    imputation_results = imputation_by_other_methods(data, method_name)

  if isinstance(imputation_results, str):
    print(f'[ERROR]: {imputation_results}')
  
  return imputation_results

def process(job_id: str) -> None:
  imputationModel = ImputationModel()

  imputation = imputationModel.get(job_id)


  method_name = imputation['method']
  method_order = imputation['order']

  if method_name not in [member.value for member in ImputationMethods]:
    imputationModel.set_error(job_id, 'no method found')
    return

  imputationModel.update_by_id(job_id, {
    'status': ImputationStatus.PROCESSING.value,
    'imputed_indexes': get_null_values_indexes(imputation['time_series'])
  })

  imputation_results = route(imputation['time_series'], method_name, method_order)

  if isinstance(imputation_results, str):
    imputationModel.set_error(job_id, imputation_results)
    return

  imputationModel.finish_imputation(job_id, imputation_results)

  return

def create(time_series: list[float], method: str, order: int | None) -> str:

  imputationModel = ImputationModel()

  id = imputationModel.create_imputation(time_series, method, order)

  return id

def get(id: str, onlyImputedData: bool = False):
  imputationModel = ImputationModel()
  result = imputationModel.get(id, onlyImputedData)

  return result