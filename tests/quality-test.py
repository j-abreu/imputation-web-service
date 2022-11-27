from pathlib import Path
import sys
import pandas as pd

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from my_utils.enums import ImputationMethods as im
from services import imputation as IMP

DATA_PATH = './data/daily-temperature.csv'
COLUMN_NAME = 'temp'

def load_data(path: str, column: str) -> pd.DataFrame:
  data = pd.read_csv(Path(path))
  return data[column]

def main() -> None:
  imputation_methods = [
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
    {
      'name': im.TIME.value,
      'order': None,
    },
    {
      'name': im.SPLINE.value,
      'order': None,
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

  data = load_data(DATA_PATH, 'temp')
  results = pd.DataFrame()

  for method in imputation_methods:
    pass 

if __name__ == '__main__':
  main()