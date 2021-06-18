# Power Ranges
## South African Energy Consumption Prediction

### Usage
1. Clone repository to local computer.
2. Install requirements.
3. Download `lstm_models.zip` from [here](https://drive.google.com/file/d/124OUIRY-a55duinCBv2iMbORoVEmb9tz/view?usp=sharing).
4. Extract `lstm_models.zip` to repository directory. Ensure the extracted data is stored in a sub-directory named `lstm_models`.
5. Run `inference.py` to host the API locally.
6. Run `client.py` and/or `Demonstation.ipynb` to check the API responses.

#### API GET requests overview
- http://127.0.0.1:5000/api/predict?meter_id=<meter_id>&csv_url=<weather_data_csv_url> -
  Returns JSON of consumption predictions and associated timestamps for prediction using model associated with passed meter ID and weather data input from the csv at the url passed.
- http://127.0.0.1:5000/api/business_ids - Returns list (JSON) of business IDs.
- http://127.0.0.1:5000/api/meter_ids?business_id=<business_id> - Returns list (JSON) of meter IDs associated with passed business ID.

#### CSV at <weather_data_csv_url> requirements
See example file [here](https://raw.githubusercontent.com/Jamie-B22/Data/main/201130_weather_feats.csv)

Requirements:
- Weather data timestamps must be of hourly intervals, covering the range the predictions are required for plus the previous 23 hours (as each input to the model required a 24h window of data)
- Columns must be named exactly as described below and units adhered to. It is recommended to use the example file as a template:
    - `captured_on_h` - timestamp, format example: `01/01/2018 02:00`
    - `surface_pressure` - ground level pressure, Pa
    - `total_precipitation` - total all forms of precipitation in interval, m
    - `total_cloud_cover` - fraction, 0-1
    - `2m_temperature_c` - 2m above ground level temperature, Celcius
    - `2m_dewpoint_temperature_c` - 2m above ground level dewpoint temperature, Celcius
    
- Weather data csv should be uploaded to a publicly available location to be accessed by a url passed to the get request.
  The csv contents are passed as raw text when the url is accessed. One solution is to use Github and use the url available to access the 'raw' page of the file.