import numpy as np

class ModelWrapper():
    def __init__(self, possible_predictions):
        self._id_space = possible_predictions


    def predict(self, user_id, limit=15):
        predicted = np.random.choice(self._id_space, 15)
        return {p: i for i, p in enumerate(predicted)}
