import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

prcp_parameters = ["temp", "humidity", "sealevelpressure", "preciptype"]

def read_data_set():
    return pd.read_csv("./ml/dataset/rainfall.csv", index_col="datetime")


def clean_data_set(raw_dataset):
    raw_dataset.index = pd.to_datetime(raw_dataset.index)
    raw_dataset['prcp_target'] = raw_dataset.shift(-1)['preciptype']
    raw_dataset = raw_dataset.iloc[:-1, :].copy()
    return raw_dataset


def split_data_set(raw_dataset):
    train = raw_dataset[:"31-12-2019"]
    test = raw_dataset["01-01-2020":]
    return train, test


class RainModel:
    def __init__(self):
        self.model = Ridge(alpha=0.1)
        self.init_model()

    def init_model(self):
        raw_data_set = read_data_set()
        raw_data_set = clean_data_set(raw_data_set)
        train_set, test_set = split_data_set(raw_data_set)
        self.train_model(train_set)
        self.run_test(test_set)

    def train_model(self, train_set):
        self.model.fit(train_set[prcp_parameters], train_set["prcp_target"])

    def run_test(self, test_set):
        prcp_predictions = self.model.predict(test_set[prcp_parameters])
        mae = mean_absolute_error(test_set["prcp_target"], prcp_predictions)
        print("Rain model error: {0}".format(mae))

    def get_prediction(self, current_set):
        df = pd.DataFrame(data={'temp': current_set[0], 'humidity': current_set[1], 'sealevelpressure': current_set[2], 'preciptype': current_set[3]}, index=[0])
        next_prediction = self.model.predict(df)
        return next_prediction[0]
