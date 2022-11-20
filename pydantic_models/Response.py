from pydantic import BaseModel, PrivateAttr, Field, constr

class ImputationError(BaseModel):
  message: str

class GetImputationResp(BaseModel):
  status: str
  hash: str
  imputed_data: list[float | None]
  imputed_indexes: list[int]
  error: None | ImputationError
  only_imputed_data: bool
  method: str
  order: str | None

class CreateImputationResp(BaseModel):
  hash: str

class ErrorResp(BaseModel):
  message: str