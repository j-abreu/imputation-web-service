from pydantic import BaseModel, PrivateAttr, Field, constr

class ImputationError(BaseModel):
  message: str

class GetImputationResp(BaseModel):
  status: str
  id: str
  imputed_time_series: list[float | None]
  imputed_indexes: list[int]
  error: None | ImputationError
  only_imputed_data: bool
  method: str
  order: str | None

class CreateImputationResp(BaseModel):
  id: str

class ErrorResp(BaseModel):
  message: str

class InternalServerErrorResp(ErrorResp):
  id: str | None