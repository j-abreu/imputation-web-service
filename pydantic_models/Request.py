from pydantic import BaseModel, PrivateAttr, Field, constr

class CreateImputationReq(BaseModel):
  values: list[float | None]
  method: str = 'mean'