from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from database.models import TimeSerie as TimeSerieModel
from pydantic_models.Response import GetImputationResp, ErrorResp, CreateImputationResp
from pydantic_models.Request import CreateImputationReq
from services import imputation
from my_utils.enums import ImputationStatus, ImputationMethods
from http import HTTPStatus

from time import sleep
import asyncio
import threading


app = Flask(__name__)
api = FlaskPydanticSpec('imputation-web-service', title='Imputation Web Service')
api.register(app)

@app.get('/home')
@api.validate(tags=['home'], resp=Response(HTTP_200=None))
def home():
  return "Hello, World!"

@app.get('/imputation/<hash>')
@api.validate(tags=['imputation'], body=None, resp=Response(HTTP_200=GetImputationResp, HTTP_400=ErrorResp, HTTP_404=None))
def get_imputation(hash: str):
  """Returns imputed time series based on the given hash"""
  if not hash:
    return '', HTTPStatus.NOT_FOUND.value
  
  time_serie = TimeSerieModel()
  result = time_serie.get_by_hash(hash)

  if result == None:
    return '', HTTPStatus.NOT_FOUND.value

  res = GetImputationResp(imputed_data=result['series'], hash=result['hash'], status=result['status'], error=result['error']).dict()

  return res, HTTPStatus.OK.value


@app.post('/imputation')
@api.validate(tags=['imputation'], body=CreateImputationReq, resp=Response(HTTP_201=CreateImputationResp, HTTP_400=ErrorResp))
def create_imputation():
  """Performs imputation on a univariate time series using many methods"""
  req = CreateImputationReq.parse_obj(request.json)

  if req.method not in [method.value for method in ImputationMethods]:
    res = ErrorResp(message='Invalid method').dict()
    return res, HTTPStatus.BAD_REQUEST.value

  if len(req.values) == 0: 
    res = ErrorResp(message='Empty time series').dict()
    return res, HTTPStatus.BAD_REQUEST.value

  job_hash = TimeSerieModel().create_imputation()

  threading.Thread(target=lambda: imputation.create_imputation(req.values, req.method, job_hash)).start()

  res = CreateImputationResp(hash=job_hash).dict()

  return res, HTTPStatus.CREATED.value

def main():
  app.run()

if __name__ == '__main__':
  main()