from . import mongodb_config as mongodb

def get_database(database_name: str = mongodb.DEFAULT_DB_NAME):
  conn = mongodb.get_connection()
  return conn[database_name]

def get_collection(database_name: str = mongodb.DEFAULT_DB_NAME, collection_name: str = mongodb.DEFAULT_COLLECTION_NAME):
  database = get_database(database_name)
  return database[collection_name]