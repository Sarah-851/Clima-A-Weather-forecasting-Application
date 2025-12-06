import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

raw_dataset = pd.read_csv("rainfall.csv", index_col="datetime")

raw_dataset.index = pd.to_datetime(raw_dataset.index)
raw_dataset['prcp_target'] = raw_dataset.shift(-1)['preciptype']
raw_dataset = raw_dataset.iloc[:-1,:].copy()

train = raw_dataset[:"31-12-2019"]
test = raw_dataset["01-01-2020":]

prcp_model = Ridge(alpha=0.1)
prcp_parameters = ["temp", "humidity", "sealevelpressure", "preciptype"]

prcp_model.fit(train[prcp_parameters], train["prcp_target"])
prcp_predictions = prcp_model.predict(test[prcp_parameters])
mae = mean_absolute_error(test["prcp_target"], prcp_predictions)

combine = pd.concat([test['prcp_target'], pd.Series(prcp_predictions)], axis=1)
combine.columns = ['actuals', 'predictions']

combine.plot()

print(raw_dataset.info())