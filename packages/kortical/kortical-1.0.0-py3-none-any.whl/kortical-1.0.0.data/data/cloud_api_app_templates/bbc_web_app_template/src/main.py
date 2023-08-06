import os
import requests
import json
import time
import logging
from pathlib import Path
from flask import Flask, request, render_template, Response

HTTP_OKAY = 200
HTTP_SERVER_ERROR = 500
HTTP_UNAUTHORIZED = 401

api_key = ''
predict_url = ''
logger = logging.getLogger(__name__)
current_dir = os.path.dirname(__file__)
templates_root_dir = str(Path(current_dir).parent)
templates_path = os.path.join(templates_root_dir, 'templates')
app = Flask(__name__, template_folder=templates_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['post'])
def bbc_predict():
    start_time = time.time()

    input_text = request.json['input_text']
    request_data = {
        'columns': ['text'],
        'data': [input_text]
    }
    response = requests.post(predict_url, data=json.dumps(request_data), headers={'Content-Type': 'application/json'})

    if response.status_code != HTTP_OKAY:
        logger.error(f'Predict call to model failed with status {response.status_code}')
        return Response(status=HTTP_SERVER_ERROR)

    response_data = json.loads(response.text)
    predicted_category_col_index = response_data['columns'].index('predicted_category')
    predicted_category = response_data['data'][0][predicted_category_col_index]
    end_time = time.time()

    logger.info(f'Completed request in {end_time - start_time} seconds.')

    return Response(predicted_category)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
