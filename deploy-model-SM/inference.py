import joblib
import os
import json

"""
model_fn
    model_dir: Diretório que contém o model.joblib que foi serializado.

    Função responsável por desserializar o modelo
"""
def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

"""
input_fn
    request_body: Body da requisição enviada ao modelo.
    request_content_type: (string) especfica o tipo de formato/variável da requisição.

    Essa função será responsável por carregar e validar os dados de entrada que serão usados para previsões.
"""
def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        request_body = json.loads(request_body)
        inpVar = request_body['Input']
        return inpVar
    else:
        raise ValueError("This model only supports application/json input")

"""
predict_fn
    input_data: Array dos dados de entrada (input_fn).
    model (sklearn model) Modelo desserializado da model_fn.

    Essa função será responsável por realizar as previsões com o modelo carregado na model_fn.
"""
def predict_fn(input_data, model):
    return model.predict(input_data)

"""
output_fn
    prediction: Valor retornado da função predict_fn.
    content_type: O tipo de conteúdo que o endpoint espera para ser retornado. Ex: JSON, string.

    Essa função será responsável por gerar o payload de retorno com as previsões.
"""

def output_fn(prediction, content_type):
    res = int(prediction[0])
    respJSON = {'Output': res}
    return respJSON