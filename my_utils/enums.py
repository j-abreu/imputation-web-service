from enum import Enum

class ImputationStatus(Enum):
  CREATED = 'created'
  PROCESSING = 'processing'
  FINISHED = 'finished'
  ERROR = 'error'

class ImputationMethods(Enum):
  # simple methods
  MEAN = 'mean'
  MEDIAN = 'median'
  MOST_FREQUEST = 'most frequent'

  # interpolation
  LINEAR = 'linear interpolation'
  TIME = 'time interpolation'
  QUADRATIC = 'quadratic interpolation'
  CUBIC = 'cubic interpolation'
  SPLINE = 'spline interpolation'
  BARYCENTRIC = 'barycentric interpolation'
  POLYNOMIAL = 'polynomial interpolation'

  #other
  MODE = 'mode'
  RANDOM = 'random'
  LOCF = 'locf'
  NOCB = 'nocb'
  NORMAL_UNIT_VARIANCE = 'normal unit variance'