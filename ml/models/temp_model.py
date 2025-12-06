import pandas as pd
import math
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
import datetime

def clean_tmp(tavg, t, torg):
    if math.isnan(torg) and not math.isnan(tavg) and not math.isnan(t):
        return (tavg * 2) - t
    else:
        return torg


def clean_tavg(tmin, tmax, tavg):
    if math.isnan(tavg) and not math.isnan(tmin) and not math.isnan(tmax):
        return (tmin + tmax) / 2
    else:
        return tavg


tmax_parameters = ["tmin", "tmax", "prcp"]
tmin_parameters = ["tmin", "tmax", "prcp"]


def read_data_set():
    return pd.read_csv('./ml/dataset/weather_dataset.csv', index_col='time')


def clean_data_set(raw_dataset):
    raw_dataset['prcp'] = raw_dataset['prcp'].fillna(0)
    raw_dataset['tmin'] = raw_dataset.apply(lambda x: clean_tmp(x['tavg'], x['tmax'], x['tmin']), axis=1)
    raw_dataset['tmax'] = raw_dataset.apply(lambda x: clean_tmp(x['tavg'], x['tmin'], x['tmax']), axis=1)
    raw_dataset['tmin'] = raw_dataset['tmin'].fillna(method='bfill')
    raw_dataset['tmax'] = raw_dataset['tmax'].fillna(method='bfill')
    raw_dataset['tavg'] = raw_dataset.apply(lambda x: clean_tavg(x['tmin'], x['tmax'], x['tavg']), axis=1)

    raw_dataset.index = pd.to_datetime(raw_dataset.index)
    raw_dataset['tmax_target'] = raw_dataset.shift(-1)['tmax']
    raw_dataset['tmin_target'] = raw_dataset.shift(-1)['tmin']
    raw_dataset = raw_dataset.iloc[:-1, :].copy()
    return raw_dataset


def split_data_set(raw_dataset):
    train = raw_dataset[:"31-12-2020"]
    test = raw_dataset["01-01-2021":]
    return train, test


class TempModel:
    def __init__(self):
        self.tmax_model = Ridge(alpha=0.1)
        self.tmin_model = Ridge(alpha=0.1)
        self.init_model()

    def init_model(self):
        raw_data_set = read_data_set()
        raw_data_set = clean_data_set(raw_data_set)
        train_set, test_set = split_data_set(raw_data_set)
        self.train_model(train_set)
        self.run_test(test_set)

    def train_model(self, train_set):
        self.tmax_model.fit(train_set[tmax_parameters], train_set["tmax_target"])
        self.tmin_model.fit(train_set[tmin_parameters], train_set["tmin_target"])

    def run_test(self, test_set):
        tmax_predictions = self.tmax_model.predict(test_set[tmax_parameters])
        tmin_predictions = self.tmin_model.predict(test_set[tmin_parameters])
        tmax_mae = mean_absolute_error(test_set["tmax_target"], tmax_predictions)
        tmin_mae = mean_absolute_error(test_set["tmin_target"], tmin_predictions)
        print("tmax model error: {0}".format(tmax_mae))
        print("tmin model error: {0}".format(tmin_mae))

    def get_prediction(self, current_set):
        df = pd.DataFrame(data={'tmin': current_set[0], 'tmax': current_set[1], 'prcp': current_set[2]}, index=[0])
        next_tmax_prediction = self.tmax_model.predict(df)
        next_tmin_prediction = self.tmin_model.predict(df)
        return next_tmin_prediction[0], next_tmax_prediction[0]
