from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors


CWD = Path(__file__).parents[0]
ALGOS = [
  'normal_unit_variance',
  'barycentric_interpolation',
  'polynomial_interpolation',
  'mode',
  'random',
  'linear_interpolation',
  'spline_interpolation',
  'locf',
  'nocb',
  'median',
  'most_frequent',
  'mean',
]
COLORS = [
  mcolors.CSS4_COLORS['lightcoral'],
  mcolors.CSS4_COLORS['darkseagreen'],
  mcolors.CSS4_COLORS['darkorange'],
  mcolors.CSS4_COLORS['royalblue'],
  mcolors.CSS4_COLORS['orangered'],
  mcolors.CSS4_COLORS['lawngreen'],
  mcolors.CSS4_COLORS['lightseagreen'],
  mcolors.CSS4_COLORS['slateblue'],
  mcolors.CSS4_COLORS['chocolate'],
  mcolors.CSS4_COLORS['goldenrod'],
  mcolors.CSS4_COLORS['steelblue'],
  mcolors.CSS4_COLORS['crimson']
]
N_USERS = [1500, 3000, 3750, 7500, 9750, 12750, 15000]
CREATE_IMP = 1
GET_IMP = 2


RESULTS_DIR = Path(CWD, 'results')

def ff(item):
  print(item)

def get_file_path_list(cur_path):
  path_list = []

  if cur_path.is_dir():
    for f in cur_path.iterdir():
      for i in get_file_path_list(f):
        path_list.append(i)
  else:
    if cur_path.suffix == '.csv':
      path_list.append(str(cur_path))
  
  return path_list

def main():
  req_types = ['post_imputation', 'get_imputation']

  results = {
    req_types[0]: {},
    req_types[1]: {}
  }

  for algo in ALGOS:
    results[req_types[0]][algo] = []
    results[req_types[1]][algo] = []

    for n_users in N_USERS:
      path = Path(CWD,
        'jmeter-results',
        algo,
        f'{n_users}-users',
        'aggregate-results.csv'
      )

      if path.is_file():
        aggregate_report = pd.read_csv(path)
        results[req_types[0]][algo].append(np.rint(float(aggregate_report.iloc[CREATE_IMP]['Error %'].replace('%', ''))))
        results[req_types[1]][algo].append(np.rint(float(aggregate_report.iloc[GET_IMP]['Error %'].replace('%', ''))))

  results[req_types[0]]['normal_unit_variance'].extend([0,  0])
  results[req_types[1]]['normal_unit_variance'].extend([0, 0])



  req_types_chart_title = {
    req_types[0]: 'Requisições de criação',
    req_types[1]: 'Requisições de recuperação dos dados'
  }

  for req_type in req_types:
    fig, ax = plt.subplots()
    bar_width = 0.72
    x = np.array([10, 20, 30, 40, 50, 60, 70])

    for i, algo in enumerate(ALGOS):
      rec = ax.bar(x - i*bar_width + (12*bar_width/2-bar_width/2), results[req_type][algo], bar_width, label=algo, color=COLORS[i])
      ax.bar_label(rec, padding=5, label_type='edge', size=7)

    ax.set_title(req_types_chart_title[req_type])
    
    ax.set_ylabel('Erro (%)')
    ax.set_xlabel('Número de usuários')
    ax.set_xticks(x, N_USERS)
    ax.legend()
    

    fig.tight_layout()
    fig.set_size_inches(18.5, 10.5)

    # plt.show()
    fig_path = str(Path(CWD, '..', 'images', f'jmeter_{req_type}.png'))
    plt.savefig(fig_path, dpi=100)
  

if __name__ == '__main__':
  main()