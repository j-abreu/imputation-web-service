import pymongo

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DEFAULT_DB_NAME = 'imputation_dev'
DEFAULT_COLLECTION_NAME = 'imputation'

def get_connection(hostname: str = MONGODB_HOST, port: int = MONGODB_PORT):
  conn = pymongo.MongoClient(hostname, port)
  return conn