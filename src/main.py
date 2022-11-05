from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from models.Response import SimpleImputationResp, ErrorResp
from models.Request import SimpleImputationReq
from controllers import imputations
from my_utils.enums import ImputationStatus, SimpleImputationMethods

app = Flask(__name__)
api = FlaskPydanticSpec('imputation-web-service', title='Imputation Web Service')
api.register(app)

@app.get('/home')
@api.validate(resp=Response(HTTP_200=None))
def home():
  return "Hello, World!"

@app.post('/imputation/simple-imputation')
@api.validate(body=SimpleImputationReq, resp=Response(HTTP_200=SimpleImputationResp, HTTP_400=ErrorResp))
def create_simple_imputation():
  """Performs simple imputation on a univariate time series using statistic methods"""
  req = SimpleImputationReq.parse_obj(request.json)

  if req.method not in [method.value for method in SimpleImputationMethods]:
    res = ErrorResp(message='Invalid method').dict()
    return res, 400

  imputed_data = imputations.simple_imputation(req.values, method=req.method)
  status = ImputationStatus.CREATED.value
  hash = '' # TODO: create hash

  res = SimpleImputationResp(imputed_data=imputed_data, status=status, hash=hash).dict()

  return res, 200

if __name__ == '__main__':
  app.run(debug=True)