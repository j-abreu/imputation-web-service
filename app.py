from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from models.Response import ImputationResp, ErrorResp
from models.Request import ImputationReq
from services import imputation
from my_utils.enums import ImputationStatus, ImputationMethods

app = Flask(__name__)
api = FlaskPydanticSpec('imputation-web-service', title='Imputation Web Service')
api.register(app)

@app.get('/home')
@api.validate(tags=['home'], resp=Response(HTTP_200=None))
def home():
  return "Hello, World!"

@app.post('/imputation')
@api.validate(tags=['interpolation'], body=ImputationReq, resp=Response(HTTP_201=ImputationResp, HTTP_400=ErrorResp))
def create_simple_imputation():
  """Performs imputation on a univariate time series using many methods"""
  req = ImputationReq.parse_obj(request.json)

  if req.method not in [method.value for method in ImputationMethods]:
    res = ErrorResp(message='Invalid method').dict()
    return res, 400

  imputed_data = imputation.perform_imputation(req.values, method=req.method)
  status = ImputationStatus.CREATED.value
  hash = '' # TODO: create hash

  res = ImputationResp(imputed_data=imputed_data, status=status, hash=hash).dict()

  return res, 201

if __name__ == '__main__':
  app.run()