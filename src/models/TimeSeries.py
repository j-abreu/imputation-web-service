from pydantic import BaseModel, PrivateAttr, Field, constr

class TimeSeries(BaseModel):
  values: list[float | None]
  _hash: str = PrivateAttr()

  def __init__(self, **data):
    super().__init__(**data)
    self._hash = '1234'