from enum import Enum

def get_composite_enum(name: str, enums: list[Enum], additional_keys_value = {}) -> Enum:
  new_composite_enum = {}
  for enum in enums:
    keys = list(enum.__members__)

    for key in keys:
      new_composite_enum[key] = enum[key].value

  for k, v in additional_keys_value.items():
    new_composite_enum[k] = v
  
  return Enum(name, new_composite_enum)

class ImputationStatus(Enum):
  CREATED = 'created'
  PROCESSING = 'processing'
  FINISHED = 'finished'
  ERROR = 'error'

class SimpleImputationMethods(Enum):
  MEAN = 'mean'
  MEDIAN = 'median'
  MOST_FREQUEST = 'most frequent'

class InterpolationImputationMethods(Enum):
  LINEAR = 'linear interpolation'
  TIME = 'time interpolation'
  QUADRATIC = 'quadratic interpolation'
  CUBIC = 'cubic interpolation'
  SPLINE_1_ORDER = '1-order spline interpolation'
  SPLINE_2_ORDER = '2-order spline interpolation'
  SPLINE_3_ORDER = '3-order spline interpolation'
  BARYCENTRIC = 'barycentric interpolation'
  POLYNOMIAL_2_ORDER = '1-order polynomial interpolation'
  POLYNOMIAL_3_ORDER = '2-order polynomial interpolation'
  POLYNOMIAL_4_ORDER = '3-order polynomial interpolation'

class OtherImputationMethods(Enum):
  MODE = 'mode'
  RANDOM = 'random'
  LOCF = 'locf'
  NOCB = 'nocb'
  NORMAL_UNIT_VARIANCE = 'normal unit variance'

ImputationMethods = get_composite_enum('ImputationMethods', [
  SimpleImputationMethods,
  InterpolationImputationMethods,
  OtherImputationMethods
  ])