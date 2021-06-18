"""
Check responses from the API setup on the localhost
Author: Jamie Bamforth
"""
import requests


def check_responses(meter_id, url):
    """Send GET request containing meter ID and the url of the weather data features to the API to retrieve and return
    response containing JSON of consumption predictions and timestamps for the given meter ID and time period in the
    weather features data."""
    payload = {'meter_id':meter_id,
               'csv_url':url}
    response_preds = requests.get('http://127.0.0.1:5000/api/predict', params=payload)
    return response_preds

def check_responses_business_ids():
    """Send GET request the API to retrieve and return response containing JSON of business IDs. This is used by front
    end to enable the businesses to be displayed for selection."""
    response = requests.get('http://127.0.0.1:5000/api/business_ids')
    return response

def check_responses_meter_ids(business_id):
    """Send GET request with a business ID to the API to retrieve and return response containing JSON of meter IDs owned
    by that business. This is used by front end to enable the businesses to be displayed for selection."""
    payload = {'business_id': str(business_id)}
    response = requests.get('http://127.0.0.1:5000/api/meter_ids', params=payload)
    return response


if __name__ == '__main__':
    """Check responses by printing JSON response."""
    print('######### Business IDs ############')
    print(check_responses_business_ids().json())

    print('######### Meter ID(s) for a Business ############')
    print(check_responses_meter_ids(393403).json())

    print('######### Predictions for Meter ID 200713 (takes ~10s) ############')
    print(check_responses(200713, 'https://raw.githubusercontent.com/Jamie-B22/Data/main/200713_weather_feats.csv').json())

    print('######### Predictions for Meter ID 201130 (takes ~10s) ############')
    print(check_responses(201130, 'https://raw.githubusercontent.com/Jamie-B22/Data/main/201130_weather_feats.csv').json())
