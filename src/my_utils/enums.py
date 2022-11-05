from enum import Enum

class ImputationStatus(Enum):
  CREATED = 'created'
  PROCESSING = 'processing'
  FINISHED = 'finished'
  ERROR = 'error'

class SimpleImputationMethods(Enum):
  MEAN = 'mean'
  MEDIAN = 'median'
  MOST_FREQUEST = 'most_frequest'