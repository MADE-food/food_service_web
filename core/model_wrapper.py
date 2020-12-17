import numpy as np
import pandas as pd

class ModelWrapper():
    def __init__(self, possible_predictions):
        self._id_space = possible_predictions
        self._predictions = pd.read_parquet('data/pred2.parquet')

        self._roller_data = pd.read_parquet('data/generated.parquet')



    def predict(self, user_id, limit=15):
        predictions = self._predictions.loc[self._predictions['customer_id']==user_id].head(limit)
        predictions.sort_values('pred', ascending=True, inplace=True)
        predictions_dict = predictions[['chain_id', 'pred']].to_dict(orient='rows')

        return {pd['chain_id']:pd['pred'] for pd in predictions_dict}

    def predict_by_roller(self, selected_restaurants):
        def IoU(list1, list2):
            i = len(list(set(list1) & set(list2)))
            u = len(list(set(list1).union(set(list2))))
            return i / u

        customers_chains = self._roller_data.groupby('customer_id')['chain_id'].apply(list)
        customers_chains = customers_chains.reset_index()

        customers_chains['iou'] = customers_chains['chain_id'].apply(lambda x: IoU(x, selected_restaurants))
        best_fit_user = customers_chains.sort_values('iou', ascending=False)['customer_id'].values[0]

        return self.predict(best_fit_user)