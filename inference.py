"""
Implement a trained model on a server using Flask to allow a REST API to be used to get predictions from the model.
Author: Jamie Bamforth
"""
import pandas as pd
from flask import Flask, request, jsonify
from flask_prediction_fn import predict_fn
from flask_cors import CORS, cross_origin
from io import StringIO
import json

app = Flask(__name__)
cors = CORS(app) # cors needed for front end implementation, so keep in
app.config['CORS_HEADERS'] = 'Content-Type'

# Currently unused but keep in for front end when developed
def file_from_req(req):
    content = req.files['file'].stream.read().decode("utf-8")
    return StringIO(content)


@app.route('/api/predict', methods=['GET'])
@cross_origin()
def predict_api():
    """Execute GET request containing meter ID and the url of the weather data features to the API to retrieve and return
    response containing JSON of consumption predictions and timestamps for the given meter ID and time period in the
    weather features data."""
    meter_id = request.args.get('meter_id')
    url = request.args.get('csv_url')
    weather_data_df = pd.read_csv(url, index_col='captured_on_h', parse_dates=True)

    timestamps, preds = predict_fn(meter_id, weather_data_df)
    print(timestamps, preds)
    output = jsonify(timestamps=timestamps, consumption=preds)
    return output

@app.route('/api/business_ids', methods=['GET'])
@cross_origin()
def business_ids_api():
    """Execute GET request the API to retrieve and return response containing JSON of business IDs. This is used by front
    end to enable the businesses to be displayed for selection."""
    with open('ids.json', 'r') as fp:
        data = json.load(fp)
    return jsonify(data['business_ids'])

@app.route('/api/meter_ids', methods=['GET'])
@cross_origin()
def meter_ids_api():
    """Execute GET request with a business ID to the API to retrieve and return response containing JSON of meter IDs owned
    by that business. This is used by front end to enable the businesses to be displayed for selection."""
    business_id = request.args.get('business_id')
    with open('ids.json', 'r') as fp:
        data = json.load(fp)
    return jsonify(data['meter_ids'][business_id])


if __name__ == '__main__':
    """Run Flask app locally."""
    app.run(host='0.0.0.0', port=5000)