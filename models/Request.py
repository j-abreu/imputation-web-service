from pydantic import BaseModel, PrivateAttr, Field, constr

class ImputationReq(BaseModel):
  values: list[float | None]

class SimpleImputationReq(ImputationReq):
  method: str = 'mean'