from ml.models.rain_model import RainModel
from ml.models.temp_model import TempModel


class ModelManager:
    def __init__(self):
        self.rain_model = RainModel()
        self.temp_model = TempModel()

    def get_models(self):
        return  self.temp_model, self.rain_model