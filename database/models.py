from tinydb import TinyDB, Query, where
from uuid import uuid4

db = TinyDB('database/db.json')


class TimeSerie:
  # TODO: implement update and update_where_hash
  def __init__(self):
    self.table = db.table('series')
  
  def insert(self, data: dict):
    hash = str(uuid4())
    data['hash'] = hash
    self.table.insert(data)

    return hash

  def get(self, id: int):
    result = self.table.get(doc_id=id)
    
    return result

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



