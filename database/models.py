from tinydb import TinyDB, Query, where
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
  
  def create_imputation(self) -> str:
    hash = str(uuid4())
    data = {
      'series': [],
      'hash': hash,
      'status': ImputationStatus.CREATED.value
    }

    self.table.insert(data)

    return hash

  def set_status(self, hash: str, status: ImputationStatus) -> None:
    result = self.table.find(where('hash') == hash)

    if len(result) == 0:
      return
    
    imputation = result[0]
    imputation['status'] = status.value

    self.table.update(imputation, where('hash') == hash)

    return

  def finish_imputation(self, hash: str, series: list[float]) -> None:

    data = {
      'series': series,
    }

    self.table.update(data, where('hash') == hash)

  def get_by_hash(self, hash: str):
    result = self.table.search(where('hash') == hash)

    if len(result) == 0:
      return None
    
    return result[0]

  def find(self, query):
    result = self.table.search(query)

    if len(result) == 0:
      return None

    return result[0]



