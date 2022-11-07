from pydantic import BaseModel, PrivateAttr, Field, constr

class ImputationResp(BaseModel):
  status: str
  hash: str
  imputed_data: list[float | None]

class ErrorResp(BaseModel):
  message: str