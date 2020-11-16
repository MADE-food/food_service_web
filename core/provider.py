import json
import pandas as pd
from .model_wrapper import ModelWrapper


class Provider():
    def __init__(self):

        with open("data/data.json", 'r') as f:
            self._data = json.load(f)

        # читаю справочник ресторанов
        self._chains_dim = pd.read_csv("data/chains_dim.csv")
        # создаю обёртку над моделью, передаю туда список возможных айди для предикта
        self._model_wrapper = ModelWrapper(self._chains_dim['chain_id'].values)


    def get_user_recommendations(self, user_id, limit=15):
        """Возвращает рекомендации пользователя"""
        # словарь айди с предиктом модели, уже сортированный по убыванию важности
        model_predictions = self._model_wrapper.predict(user_id, limit)
        predicted_ids = list(model_predictions.keys())

        # Вытаскиваю из справочника только тех, кого рекомендовала модель
        predicted_chains = self._chains_dim.loc[self._chains_dim['chain_id'].isin(predicted_ids)]
        predicted_chains['rank'] = predicted_chains['chain_id'].map(model_predictions)
        predicted_chains.sort_values(by='rank', inplace=True)
        result = predicted_chains.to_dict(orient='records')
        return result

    def get_user_history(self, user_id, limit=7):
        """Возвращает историю пользователя"""
        result = self._chains_dim.sample(limit).to_dict(orient='records')
        return result

    def get_restaraunt_info(self, restaurant_id):
        """Возвращает информацию по выбранному ресторану"""
        found_chain = self._chains_dim.loc[self._chains_dim['chain_id']==restaurant_id]
        result = found_chain.to_dict()
        return result

    def __get_chains(self, limit=15):
        return self._chains_dim.sample(limit)


class RestaurantInfo(dict):
    def __init__(self):
        pass

    def __getattr__(self, attr):
        return self[attr]
