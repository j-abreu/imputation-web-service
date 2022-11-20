from tinydb import TinyDB, Query, where
import numpy as np
from my_utils.enums import ImputationStatus
from uuid import uuid4

db = TinyDB('database/db.json')


class TimeSerie:
  # TODO: implement update and update_where_hash
  def __init__(self):
    self.table = db.table('series')
  
  def get(self, id: int):
    result = self.table.get(doc_id=id)
    
    return result

  def insert(self, data: dict):
    self.table.insert(data)

    return hash
  
  def create_imputation(self, method: str, order: int = None) -> str:
    hash = str(uuid4())
    data = {
      'series': [],
      'imputed_indexes': [],
      'hash': hash,
      'status': ImputationStatus.CREATED.value,
      'error': None,
      'method': method,
      'order': order
    }

    self.table.insert(data)

    return hash

  def set_status(self, hash: str, status: ImputationStatus) -> None:

    self.table.update({'status': status.value}, where('hash') == hash)

    return

  def finish_imputation(self, hash: str, series: list[float]) -> None:

    data = {
      'series': series,
      'status': ImputationStatus.FINISHED.value
    }

    self.table.update(data, where('hash') == hash)
  
  def set_error(self, hash: str, error_message: str) -> None:
    self.table.update({'status': ImputationStatus.ERROR.value, 'error': {"message": error_message}}, where('hash') == hash)

  def get_by_hash(self, hash: str, onlyImputed: bool = False):
    result = self.table.search(where('hash') == hash)

    if len(result) == 0:
      return None
    
    if not onlyImputed:
      return result[0]

    document = result[0]
    imputed_data = np.array(document['series'])
    imputed_indexes = document['imputed_indexes']

    document['series'] = list(imputed_data[imputed_indexes])

    return document

  def find(self, query):
    result = self.table.search(query)

    if len(result) == 0:
      return None

    return result[0]

  def update_where_hash(self, hash: str, data: dict):
    self.table.update(data, where('hash') == hash)

    return


