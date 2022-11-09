from tinydb import TinyDB, Query, where

db = TinyDB('database/db.json')

def insert_data(table: str, data: dict):
  Table = db.table(table)
  return Table.insert(data)

def get(table: str, id: int):
  Table = db.table(table)
  return Table.get(doc_id=id)

def find(table: str, query):
  Table = db.table(table)
  imputed_data = Table.search(query)

  if len(imputed_data) == 0:
    return None

  return imputed_data[0]
