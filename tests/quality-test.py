import pandas as pd
import numpy as np
import sys
import time
import math
from datetime import datetime
from pathlib import Path
from matplotlib import pyplot as plt

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from my_utils.enums import ImputationMethods as im
from services import imputation as imp


CWD = Path(__file__).parents[0]
FILE_PATH = './data/daily-temperature.csv'
COLUMN_COMPLETE = 'temp'
COLUMN_MISS = 'temp_miss'
NUM_RUNS = 30
# TODO: Verify time interpolation method error
METHODS = [
    {
      'name': im.MEAN.value,
      'order': None,
    },
    {
      'name': im.MEDIAN.value,
      'order': None,
    },
    {
      'name': im.MOST_FREQUENT.value,
      'order': None,
    },
    {
      'name': im.LINEAR.value,
      'order': None,
    },
    # {
    #   'name': im.TIME.value,
    #   'order': None,
    # },
    {
      'name': im.SPLINE.value,
      'order': 3,
    },
    {
      'name': im.BARYCENTRIC.value,
      'order': None,
    },
    {
      'name': im.POLYNOMIAL.value,
      'order': 3,
    },
    {
      'name': im.MODE.value,
      'order': None,
    },
    {
      'name': im.RANDOM.value,
      'order': None,
    },
    {
      'name': im.LOCF.value,
      'order': None,
    },
    {
      'name': im.NOCB.value,
      'order': None,
    },
    {
      'name': im.NORMAL_UNIT_VARIANCE.value,
      'order': None,
    },
  ]

def load_data(path: str, column: str) -> list[float]:
  path = Path(CWD, path)
  data = pd.read_csv(path)

  return data[column].tolist()

def save_results(results: pd.DataFrame):
  file_name = f'results_{str(datetime.now())}.csv'.replace(':', '-')
  path = Path(Path(__file__).parents[0], 'quality-test-results', file_name)
  results.to_csv(path, index=False)

def replace_nan_with_none(x: list[float]):
  x_np = np.array(x)
  x_result = np.where(np.isnan(x_np), None, x_np).tolist()
  return x_result

def RMSE(predictions: list[float], targets: list[float]) -> float:
  predictions_np, targets_np = np.array(predictions), np.array(targets)

  return np.sqrt(((predictions_np - targets_np) ** 2).mean())

def MAE(predictions: list[float], targets: list[float]) -> float:
  predictions_np, targets_np = np.array(predictions), np.array(targets)

  return np.mean(np.abs(targets_np - predictions_np))

def MARE(predictions: list[float], targets: list[float]) -> float:
  predictions_np, targets_np = np.array(predictions), np.array(targets)

  eps = np.finfo(float).eps

  return np.mean(np.abs(targets_np - predictions_np) / np.abs(np.maximum(eps, targets_np)))


def main() -> None:
  data_miss, data_complete = load_data(FILE_PATH, COLUMN_MISS), load_data(FILE_PATH, COLUMN_COMPLETE)

  results = []
  for method in METHODS:
    partial_results = {
      'time': [],
      'mae': [],
    }

    print(f"[START] -> method: {method['name']} - order: {method['order']}")
    print('[', end='')
    for i in range(NUM_RUNS):
      print('-', end='')
      start_ms = time.time() * 1000
      imputation_results = imp.route(data_miss, method['name'], method['order'])
      end_ms = time.time() * 1000


      time_diff_ms = end_ms - start_ms
      partial_results['time'].append(time_diff_ms)
    print(']')


    mae_result = MAE(imputation_results, data_complete)
    mare_result = MARE(imputation_results, data_complete)
    print('mare:', mare_result)

    mean_time = np.mean(partial_results['time'])
    std_time = np.std(partial_results['time'])

    results.append([method['name'], method['order'], mae_result, mare_result, mean_time, std_time])
    print(f"[FINISH] -> method: {method['name']} - time: {time_diff_ms}")
    if i == 2:
      break
  
  columns = ['method', 'order', 'MAE', 'MARE', 'time', 'std']
  results_df = pd.DataFrame(results, columns=columns)
  save_results(results_df)

if __name__ == '__main__':
  main()
  