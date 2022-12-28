from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors


CWD = Path(__file__).parents[0]
ALGOS = [
  # 'normal_unit_variance',
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
N_USERS = [1000, 2000, 4000, 6000, 10000]
CREATE_IMP = 1
GET_IMP = 2


RESULTS_DIR = Path(CWD, 'results', 'version_B')

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

def get_last_column():
  rows = []
  for algo in ALGOS:
    for _ in range(len(N_USERS)):
      rows.append(algo)
  return rows

def boxplot(results):
  cols = ['Algoritmo', 'Número de Usuários', 'Tempo Médio (ms)']
  get_results_np = np.array([]).reshape(0, len(cols))
  post_results_np = np.array([]).reshape(0, len(cols))

  for i, algo in enumerate(ALGOS):
    for j, n_users in enumerate(N_USERS):
      # cols: algo, n_users, avg_time
      row = np.array([[algo, n_users, results['get_imputation'][n_users][i]]])
      get_results_np = np.concatenate((get_results_np, row), axis=0)

      row = np.array([[algo, n_users, results['post_imputation'][n_users][i]]])
      post_results_np = np.concatenate((post_results_np, row), axis=0)
  
  # last_column = get_last_column()
  # get_results_df['X'] = pd.Series(last_column)
  get_results_df = pd.DataFrame(get_results_np, columns=cols)
  post_results_df = pd.DataFrame(post_results_np, columns=cols)

  get_results_df['Tempo Médio (ms)'] = get_results_df['Tempo Médio (ms)'].astype('float')
  get_results_df['Número de Usuários'] = get_results_df['Tempo Médio (ms)'].astype('float')

  post_results_df['Tempo Médio (ms)'] = post_results_df['Tempo Médio (ms)'].astype('float')
  post_results_df['Número de Usuários'] = post_results_df['Tempo Médio (ms)'].astype('float')

  boxplot_get = get_results_df.boxplot(by='Algoritmo', column=['Tempo Médio (ms)'], grid=False, rot=60, fontsize=35, figsize=(30, 18))
  boxplot_get.set_ylabel('Tempo Médio (ms)', fontsize=35)
  boxplot_get.set_xlabel('Algoritmos', fontsize=35)
  boxplot_get.set_title('Tempo Médio em Milissegundos por Algoritmo para Requisições de Recuperação')
  boxplot_get.title.set_size(30)
  plt.tight_layout(pad=2)

  fig_path_get = str(Path(CWD, '..', 'images', f'get_boxplot.png'))

  fig_get = boxplot_get.get_figure()
  fig_get.savefig(fig_path_get)

  boxplot_post = post_results_df.boxplot(by='Algoritmo', column=['Tempo Médio (ms)'], grid=False, rot=60, fontsize=35, figsize=(30, 18))
  boxplot_post.set_ylabel('Tempo Médio (ms)', fontsize=35)
  boxplot_post.set_xlabel('Algoritmos', fontsize=35)
  boxplot_post.set_title('Tempo Médio em Milissegundos por Algoritmo para Requisições de Criação')
  boxplot_post.title.set_size(30)
  plt.tight_layout(pad=2)

  fig_path_post = str(Path(CWD, '..', 'images', f'post_boxplot.png'))

  fig_post = boxplot_post.get_figure()
  fig_post.savefig(fig_path_post)

def main():
  req_types = ['post_imputation', 'get_imputation']

  results = {
    req_types[0]: {},
    req_types[1]: {}
  }

  for n_users in N_USERS:
    results[req_types[0]][n_users] = []
    results[req_types[1]][n_users] = []

    for algo in ALGOS:
      path = Path(CWD,
        'jmeter-results',
        'version_B',
        algo,
        f'{n_users}',
        'aggregate-results.csv'
      )

      if path.is_file():
        aggregate_report = pd.read_csv(path)
        results[req_types[0]][n_users].append(int(aggregate_report.iloc[CREATE_IMP]['Average']))
        results[req_types[1]][n_users].append(int(aggregate_report.iloc[GET_IMP]['Average']))

  req_types_chart_title = {
    req_types[0]: 'Requisições de criação',
    req_types[1]: 'Requisições de recuperação dos dados'
  }

  boxplot(results)
  return

  for req_type in req_types:
    fig, ax = plt.subplots()
    bar_width = 0.72
    x = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])

    for i, n_users in enumerate(N_USERS):
      rec = ax.bar(x - i*bar_width + (5*bar_width/2-bar_width/2), results[req_type][n_users], bar_width, label=f'{n_users} usuários')
      ax.bar_label(rec, padding=5, label_type='edge', size=7)

    ax.set_title(req_types_chart_title[req_type])
    
    ax.set_ylabel('Erro (%)')
    ax.set_xlabel('Algoritmos')
    ax.set_xticks(x, ALGOS)
    ax.legend()
    

    fig.tight_layout()
    fig.set_size_inches(18.5, 10.5)

    # plt.show()
    fig_path = str(Path(CWD, '..', 'images', f'jmeter_{req_type}.png'))
    plt.savefig(fig_path, dpi=100)
  

if __name__ == '__main__':
  main()