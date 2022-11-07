from pydantic import BaseModel, PrivateAttr, Field, constr

class ImputationReq(BaseModel):
  values: list[float | None]
  method: str = 'mean'