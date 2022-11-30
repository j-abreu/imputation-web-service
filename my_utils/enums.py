from enum import Enum

def get_composite_enum(name: str, enums: list[Enum], additional_keys_value: dict = {}) -> Enum:
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
  MOST_FREQUENT = 'most frequent'

class InterpolationImputationMethods(Enum):
  LINEAR = 'linear interpolation'
  TIME = 'time interpolation'
  SPLINE = 'spline interpolation'
  BARYCENTRIC = 'barycentric interpolation'
  POLYNOMIAL = 'polynomial interpolation'

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