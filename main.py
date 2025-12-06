import pandas as pd
import math
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error


def clean_tmp(tavg, t, torg):
    if math.isnan(torg) and not math.isnan(tavg) and not math.isnan(t):
        return (tavg * 2) - t
    else:
        return torg


def clean_tavg(tmin, tmax, tavg):
    if math.isnan(tavg) and not math.isnan(tmin) and not math.isnan(tmax):
        return (tmin + tmax)/2
    else:
        return tavg

# tt = pd.DataFrame(data, columns=['tmin', 'tmax', 'prcp')
# load dataset
raw_dataset = pd.read_csv('weather_dataset.csv', index_col='time')

# data cleanup
raw_dataset['prcp'] = raw_dataset['prcp'].fillna(0)
raw_dataset['tmin'] = raw_dataset.apply(lambda x: clean_tmp(x['tavg'], x['tmax'], x['tmin']), axis=1)
raw_dataset['tmax'] = raw_dataset.apply(lambda x: clean_tmp(x['tavg'], x['tmin'], x['tmax']), axis=1)
raw_dataset['tmin'] = raw_dataset['tmin'].fillna(method='bfill')
raw_dataset['tmax'] = raw_dataset['tmax'].fillna(method='bfill')
raw_dataset['tavg'] = raw_dataset.apply(lambda x: clean_tavg(x['tmin'], x['tmax'], x['tavg']), axis=1)

# prepare dataset
raw_dataset.index = pd.to_datetime(raw_dataset.index)
raw_dataset['tmax_target'] = raw_dataset.shift(-1)['tmax']
raw_dataset['tmin_target'] = raw_dataset.shift(-1)['tmin']
raw_dataset = raw_dataset.iloc[:-1,:].copy()

# prepare model
train = raw_dataset[:"31-12-2020"]
test = raw_dataset["01-01-2021":]

# tmax
tmax_model = Ridge(alpha=0.1)
tmax_parameters = ["tmin", "tmax", "prcp"]

# tmin
tmin_model = Ridge(alpha=0.1)
tmin_parameters = ["tmin", "tmax", "prcp"]


# train model
tmax_model.fit(train[tmax_parameters], train["tmax_target"])
tmin_model.fit(train[tmin_parameters], train["tmin_target"])

# predict
tmax_predictions = tmax_model.predict(test[tmax_parameters])
tmin_predictions = tmin_model.predict(test[tmin_parameters])

# test accuracy
mean_absolute_error(test["tmax_target"], tmax_predictions)
mean_absolute_error(test["tmin_target"], tmin_predictions)

combine = pd.concat([test['tmax_target'], pd.Series(tmax_predictions)], axis=1)
combine.columns = ['actuals', 'predictions']

combine.plot()

combine = pd.concat([test['tmin_target'], pd.Series(tmin_predictions)], axis=1)
combine.columns = ['actuals', 'predictions']

combine.plot()

print(raw_dataset.info())
# tt = pd.DataFrame(data=[[27, 36, 0]], columns=[['tmin','tmax','prcp']])