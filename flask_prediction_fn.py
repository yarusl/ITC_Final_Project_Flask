"""
Author: Jamie Bamforth
Date created 15/06/2021

Functions required to take an input of weather feature data at hourly intervals, along with a meter id, and outputs the
predicted power consumption over the period the weather data is provided for. Note that a window of the previous 24h of
weather data is required for each prediction, so weather features must be provided for the period that predictions are
required for, plus the previous 23 hours.

Dependencies include:
1) weather data - from url of raw csv passed to GET request
2) model for meter - in directory SAVED_MODELS_DIR_FILEPATH, retrieved using meter_id passed to GET request
3) JSON of scaling parameters - at PARAMS_JSON_FILEPATH
4) csv of public holiday dates - at PH_FILEPATH
"""



import pandas as pd
import numpy as np
import tensorflow as tf
import json

PH_FILEPATH = 'za_public_holidays_1990_2030.csv'
PARAMS_JSON_FILEPATH = 'scaling_params.json'
SAVED_MODELS_DIR_FILEPATH = 'lstm_models/'

TIMESTEPS = 24

FEATS_ORDER = ['Day sin', 'Day cos', 'Week sin', 'Week cos',
               'surface_pressure', 'total_precipitation', 'total_cloud_cover',
               '2m_temperature_c', '2m_dewpoint_temperature_c', 'public_holiday']


def add_seasonality_feats(data):
    """Takes in a dataframe with a Timestamp as an index and returns the same dataframe with 4 new columns containing
        sine and cosine wave transformations of the index with periods of 1 day and 1 week"""
    day = 24 * 60 * 60
    week = day * 7

    timestamp_s = (data.index - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")

    data['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    data['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    data['Week sin'] = np.sin(timestamp_s * (2 * np.pi / week))
    data['Week cos'] = np.cos(timestamp_s * (2 * np.pi / week))

    return data


def add_ph(data):
    """Takes in a dataframe with a Timestamp as an index and returns the same dataframe with 1 new column containing a
    binary feature indicating whether the day is a public holiday"""
    ph_dates = pd.read_csv(PH_FILEPATH, index_col='public_holiday_dates', parse_dates=True).index.date
    data['public_holiday'] = (pd.Series(data.index.date).isin(ph_dates) * 1).values
    return data


def std_scale_input(meter_id, data):
    """Takes in a dataframe and standard scales features according to the feature names, means and standard deviations
    provided by the JSON at PARAMS_JSON_FILEPATH same dataframe with scaled features returned"""
    with open(PARAMS_JSON_FILEPATH, 'r') as fp:
        d = json.load(fp)
    scaled_feats = d['feats']
    means = pd.Series(d[str(meter_id)]['means'], index=scaled_feats)
    std_devs = pd.Series(d[str(meter_id)]['std_devs'], index=scaled_feats)
    data[scaled_feats] = (data[scaled_feats] - means) / std_devs
    return data


def reshape_to_input_timesteps(data, feats_order, timesteps=1):
    """Takes in a dataframe and returns a Numpy array of shape (samples, timesteps, features) that can be used as the
    input to the model for prediction"""
    X = data[feats_order].values
    # reshape input to be 3D (samples, timesteps, features)
    X = X.reshape((X.shape[0], 1, X.shape[1]))
    X_tmp = X.copy()
    for step in range(timesteps - 1):
        X = np.hstack([X[1:, :, :], X_tmp[:-(step + 1), :, :]])
    return X


def predict_fn(meter_id, weather_data_df):
    """Takes an input of weather feature data at hourly intervals, along with a meter id, and returns the
    a dataframe of predicted power consumption over the period the weather data is provided for.

    Note that a window of the previous 24h of weather data is required for each prediction, so weather features must be
    provided for the period that predictions are required for, plus the previous 23 hours."""
    df = add_seasonality_feats(weather_data_df)
    df = add_ph(df)
    df = std_scale_input(meter_id, df)
    X = reshape_to_input_timesteps(df, FEATS_ORDER, TIMESTEPS)
    model = tf.keras.models.load_model(SAVED_MODELS_DIR_FILEPATH + str(meter_id))
    preds = model.predict(X).reshape(1,-1)[0].tolist()
    timestamps = list(df.index[TIMESTEPS - 1:])
    del model
    return timestamps, preds

