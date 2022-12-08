import numpy as np
from . import db
from my_utils.enums import ImputationStatus
from uuid import uuid4
from pymongo import ReturnDocument
from bson.objectid import ObjectId

DB_NAME = 'imputation_dev'
COLLECTION_NAME = 'imputation'

class ImputationModel:
  def __init__(self):
    self.collection = db.get_collection(COLLECTION_NAME)
  
  def add_str_id(self, document):
    document['id'] = str(document['_id'])
    return document

  def insert_one(self, data: dict):
    result = self.collection.insert_one(data)

    return str(result.inserted_id)
    
  def get(self, id: int, only_imputed_data: bool = False):
    try:
      document = self.collection.find_one({'_id': ObjectId(id)})

      if document is None or only_imputed_data is False:
        return self.add_str_id(document)
      
      if document['status'] != ImputationStatus.FINISHED.value:
        document['imputed_indexes'] = []
        return self.add_str_id(document)

      imputed_data = np.array(document['imputed_time_series'])
      imputed_indexes = document['imputed_indexes']
      document['imputed_time_series'] = list(imputed_data[imputed_indexes])

      return self.add_str_id(document)
    except Exception as e:
      return None
  
  def find(self, where: dict) -> dict:
    result = self.collection.find(where)
    return self.add_str_id(result)
  
  def find_one(self, where: dict) -> dict:
    result = self.collection.find_one(where)

    return self.add_str_id(result)

  def update(self, data: dict, where: dict):
    result = self.collection.find_one_and_update(
      where,
      {"$set": data},
      return_document=ReturnDocument.AFTER
    )

    return self.add_str_id(result)
  
  def update_by_id(self, id: str, data: dict) -> dict:
    result = self.collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {
        "$set": data
      },
      return_document=ReturnDocument.AFTER
    )

    return self.add_str_id(result)
  
  def create_imputation(self, time_series: list[float], method: str, order: int = None) -> str:
    data = {
      'time_series': time_series,
      'imputed_time_series': [],
      'imputed_indexes': [],
      'status': ImputationStatus.CREATED.value,
      'error': None,
      'method': method,
      'order': order
    }

    result = self.collection.insert_one(data)

    return str(result.inserted_id)

  def set_status(self, id: str, status: ImputationStatus) -> dict:
    result = self.collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {
        "$set": {
          "status": status.value
        }
      },
      return_document=ReturnDocument.AFTER

    )

    return self.add_str_id(result)

  def finish_imputation(self, id: str, series: list[float]) -> dict:

    data = {
      'imputed_time_series': series,
      'status': ImputationStatus.FINISHED.value
    }

    result = self.collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {"$set": data},
      return_document=ReturnDocument.AFTER

    )

    return self.add_str_id(result)
  
  def set_error(self, id: str, error_message: str) -> dict:
    new_data = {
      'status': ImputationStatus.ERROR.value,
      'error': {"message": error_message}
    }

    result = self.collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {"$set": new_data},
      return_document=ReturnDocument.AFTER
    )
    
    return self.add_str_id(result)
