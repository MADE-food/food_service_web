import numpy as np
import pandas as pd

class ModelWrapper():
    def __init__(self, possible_predictions):
        self._id_space = possible_predictions
        self._predictions = pd.read_parquet('data/pred2.parquet')



    def predict(self, user_id, limit=15):
        predictions = self._predictions.loc[self._predictions['customer_id']==user_id].head(limit)
        predictions.sort_values('pred', ascending=False, inplace=True)

        return {p: i for i, p in enumerate(predictions['chain_id'].values)}