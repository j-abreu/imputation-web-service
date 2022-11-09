from pydantic import BaseModel, PrivateAttr, Field, constr

class GetImputationResp(BaseModel):
  status: str
  hash: str
  imputed_data: list[float | None]

class CreateImputationResp(BaseModel):
  hash: str

class ErrorResp(BaseModel):
  message: str