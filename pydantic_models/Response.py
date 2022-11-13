from pydantic import BaseModel, PrivateAttr, Field, constr

class ImputationError(BaseModel):
  message: str

class GetImputationResp(BaseModel):
  status: str
  hash: str
  imputed_data: list[float | None]
  error: None | ImputationError

class CreateImputationResp(BaseModel):
  hash: str

class ErrorResp(BaseModel):
  message: str