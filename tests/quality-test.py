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
NUM_RUNS = 100
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

colors = {
  'blue': '#557ad8',
  'green': '#40f91f',
  'red': '#f93f3f'
}

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

def get_only_missing(data_miss, data_complete):
  only_missing = []
  for i in range(len(data_complete)):
    if not data_miss[i]:
      only_missing.append(data_complete[i])
    else:
      only_missing.append(None)
  
  return only_missing

def plot_time_series(data_miss, data_complete):
  data_miss = replace_nan_with_none(data_miss)
  only_missing = get_only_missing(data_miss, data_complete)

  plt.figure(figsize=(10, 6), dpi=100)

  # plot missing
  plt.plot(np.arange(len(data_complete)), data_complete, marker='None', color=colors['blue'])
  plt.plot(np.arange(len(data_miss)), data_miss, marker='.', color=colors['blue'], linestyle = 'None', label='Valor conhecido')
  plt.plot(np.arange(len(only_missing)), only_missing, marker='x', color=colors['red'], linestyle = 'None', label='Valor removido')
  plt.xlabel('Dias')
  plt.ylabel('Temperatura (°C)')
  plt.legend()
  plt.tight_layout(pad=2)
  plt.title('Temperatura média em Belém-PA ao longo dos dias com valores faltantes')

  fig_path = str(Path(CWD, '..', 'images', f'daily_temperature.png'))
  plt.savefig(fig_path, dpi=100)

  # plot imputed points
  imputation_results = imp.route(data_miss, 'linear interpolation', None)
  only_imputed = get_only_missing(data_miss, imputation_results)


  plt.figure(figsize=(10, 6), dpi=100)

  plt.plot(np.arange(len(data_complete)), data_complete, marker='None', color=colors['blue'])
  plt.plot(np.arange(len(data_miss)), data_miss, marker='.', color=colors['blue'], linestyle = 'None', label='Valor conhecido')
  plt.plot(np.arange(len(only_missing)), only_missing, marker='x', color=colors['red'], linestyle = 'None', label='Valor removido')
  # plt.plot(np.arange(len(imputation_results)), imputation_results, marker='None', markeredgecolor=colors['green'], markerfacecolor=colors['green'], color=colors['blue'], linestyle = '--', linewidth=1)
  plt.plot(np.arange(len(only_imputed)), only_imputed, marker='d', color=colors['green'], linestyle = 'None', label='Valor imputado usando Linear Interpolation')
  plt.xlabel('Dias')
  plt.ylabel('Temperatura (°C)')
  plt.legend()
  plt.tight_layout(pad=2)

  plt.title('Temperatura média em Belém-PA ao longo dos dias com valores imputados')

  fig_path = str(Path(CWD, '..', 'images', f'imputed_temperature.png'))
  plt.savefig(fig_path, dpi=100)



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


    mae_result = np.round(MAE(imputation_results, data_complete), 5)
    # mare_result = MARE(imputation_results, data_complete)
    # print('mare:', mare_result)

    mean_time = np.round(np.mean(partial_results['time']), 5)
    std_time = np.round(np.std(partial_results['time']), 5)

    results.append([method['name'], method['order'], mae_result, mean_time, std_time])
    print(f"[FINISH] -> method: {method['name']} - time: {time_diff_ms}")
    if i == 2:
      break
  
  columns = ['method', 'order', 'MAE', 'time', 'std']
  results_df = pd.DataFrame(results, columns=columns)
  save_results(results_df)

if __name__ == '__main__':
  main()
  