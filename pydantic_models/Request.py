from pydantic import BaseModel, PrivateAttr, Field, constr

class CreateImputationReq(BaseModel):
  time_series: list[float | None]
  method: str = 'mean'
  order: int | None