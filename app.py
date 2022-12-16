from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic_models.Response import GetImputationResp, ErrorResp, CreateImputationResp, InternalServerErrorResp
from pydantic_models.Request import CreateImputationReq
from services import imputation
from my_utils.enums import ImputationMethods
from http import HTTPStatus
import threading
from random import randint

app = Flask(__name__)
api = FlaskPydanticSpec('imputation-web-service', title='Imputation Web Service')
api.register(app)

@app.get('/home')
@api.validate(tags=['home'], resp=Response(HTTP_200=None))
def home():
  return "Hello, World!"

@app.get('/imputation/<id>')
@api.validate(tags=['imputation'], body=None, resp=Response(HTTP_200=GetImputationResp, HTTP_400=ErrorResp, HTTP_500=InternalServerErrorResp, HTTP_404=None))
def get_imputation(id: str):
  """Returns imputed time series based on the given id"""
  if not id:
    return '', HTTPStatus.NOT_FOUND.value

  onlyImputedData = request.args.get('onlyImputed')

  if onlyImputedData == None:
    onlyImputedData = False
  else:
    onlyImputedData = True if onlyImputedData.lower() == 'true' else False
  
  result = imputation.get(id, onlyImputedData)

  if result == None:
    return '', HTTPStatus.NOT_FOUND.value

  if result['error']:
    res = InternalServerErrorResp(
      message=result['error']['message'],
      id=result['id']).dict()
    return res, HTTPStatus.INTERNAL_SERVER_ERROR

  res = GetImputationResp(
    imputed_time_series=result['imputed_time_series'],
    id=result['id'],
    status=result['status'],
    error=result['error'],
    imputed_indexes=result['imputed_indexes'],
    method=result['method'],
    order=result['order'],
    only_imputed_data=onlyImputedData).dict()

  return res, HTTPStatus.OK.value


@app.post('/imputation')
@api.validate(tags=['imputation'], body=CreateImputationReq, resp=Response(HTTP_201=CreateImputationResp, HTTP_400=ErrorResp))
def create_imputation():
  """Performs imputation on a univariate time series using many methods"""
  req = CreateImputationReq.parse_obj(request.json)

  if req.method not in [method.value for method in ImputationMethods]:
    res = ErrorResp(message='Invalid method').dict()
    return res, HTTPStatus.BAD_REQUEST.value

  method_with_order = [ImputationMethods.SPLINE.value, ImputationMethods.POLYNOMIAL.value]
  allowed_orders = [1, 2, 3, 4, 5] # TODO: verify allowed orders
  method_order = None

  if req.method in method_with_order:
    if req.order is None:
      res = ErrorResp(message='This method requires an order argument').dict()
      return res, HTTPStatus.BAD_REQUEST.value
    
    if req.order in allowed_orders:
      method_order = req.order
    else:
      res = ErrorResp(message=f'Order must in {allowed_orders}').dict()
      return res, HTTPStatus.BAD_REQUEST.value

  if len(req.time_series) == 0: 
    res = ErrorResp(message='Empty time series').dict()
    return res, HTTPStatus.BAD_REQUEST.value

  method = {
    'name': req.method,
    'order': method_order
  }

  job_id = imputation.create(req.time_series, method['name'], method['order'])

  # imputation_data = {
  #   'time_series': req.time_series,
  #   'method': method['name'],
  #   'order': method['order']
  # }

  # threading.Thread(target=lambda: imputation.process(job_id, imputation_data)).start()

  res = CreateImputationResp(id=job_id).dict()

  return res, HTTPStatus.CREATED.value

def main():
  # Start Imputation Processor
  is_running = True
  t1 = threading.Thread(target=imputation.loop, args=(randint(0, 999), lambda: is_running))
  t1.start()

  # Start Flask App
  app.run(host='0.0.0.0', port=5000)
  is_running = False
  t1.join()

if __name__ == '__main__':
  main()