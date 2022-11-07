from enum import Enum

class ImputationStatus(Enum):
  CREATED = 'created'
  PROCESSING = 'processing'
  FINISHED = 'finished'
  ERROR = 'error'

class SimpleImputationMethods(Enum):
  MEAN = 'mean'
  MEDIAN = 'median'
  MOST_FREQUEST = 'most_frequent'

class ImputationByInterpolationMethods(Enum):
  LINEAR = 'linear'
  TIME = 'time'
  QUADRATIC = 'quadratic'
  CUBIC = 'cubic'
  SPLINE = 'spline'
  BARYCENTRIC = 'barycentric'
  POLYNOMIAL = 'polynomial'