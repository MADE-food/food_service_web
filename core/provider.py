import json
import pandas as pd
import numpy as np
import json
from .model_wrapper import ModelWrapper


def have_intersection(a1, a2):
    """Проверяет, есть пересечение двух массивов. Нужно для фильтар по типу продуктов"""
    return len(set.intersection(set(a1), set(a2))) > 0


class Provider():
    def __init__(self):
        # читаю справочник ресторанов
        data = pd.read_csv("data/chains_dim.csv")
        data['product_group_ids'] = data['product_group_ids'].apply(lambda x: json.loads(x) if x and pd.notna(x) else []) #массив групп продуктов из стринга
        self._chains_dim = data

        # создаю обёртку над моделью, передаю туда список возможных айди для предикта
        self._model_wrapper = ModelWrapper(self._chains_dim['chain_id'].values)

    def get_user_recommendations(self, user_id, limit=15, filter_products=[]):
        """Возвращает рекомендации пользователя"""
        # словарь айди с предиктом модели, уже сортированный по убыванию важности
        model_predictions = self._model_wrapper.predict(user_id)
        predicted_ids = list(model_predictions.keys())

        # Вытаскиваю из справочника только тех, кого рекомендовала модель
        predicted_chains = self._chains_dim \
            .loc[
                    self._chains_dim['chain_id'].isin(predicted_ids)
                    &
                    self._chains_dim['product_group_ids'].apply(lambda x: have_intersection(x, filter_products))
        ]
        # Присваиваем ранк и сортируем по нему
        predicted_chains['rank'] = predicted_chains['chain_id'].map(model_predictions)
        predicted_chains.sort_values(by='rank', inplace=True)

        # отрезаю по лимиту
        predicted_chains = predicted_chains.head(limit)

        # в дикт
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
        """Возврщает набор чейнов"""
        return self._chains_dim.sample(limit)

    def get_product_ids(self):
        product_ids = list(set(np.concatenate(self._chains_dim['product_group_ids'].values)))
        return [int(x) for x in product_ids]

class RestaurantInfo(dict):
    def __init__(self):
        pass

    def __getattr__(self, attr):
        return self[attr]
