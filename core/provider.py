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
        data = pd.read_csv("data/chains_dim.csv", dtype={'default_product_group_id':pd.Int64Dtype()})

        data['product_group_ids'] = data['product_group_ids'].apply(lambda x: json.loads(x) if x and pd.notna(x) else []) #массив групп продуктов из стринга
        self._chains_dim = data

        # читаю справочник продуктов
        data = pd.read_csv('data/products_dim.csv')
        self._products_dim = data.to_dict(orient='records')

        # читаю пользовательскую историю
        self._history = pd.read_parquet('data/history.parquet')

        # создаю обёртку над моделью, передаю туда список возможных айди для предикта
        self._model_wrapper = ModelWrapper(self._chains_dim['chain_id'].values)

    def __enrich_predictions(self, model_predictions, filtered_chains):
        predicted_ids = list(model_predictions.keys())
        predicted_chains = filtered_chains.loc[filtered_chains['chain_id'].isin(predicted_ids)]

        predicted_chains['rank'] = predicted_chains['chain_id'].map(model_predictions)
        predicted_chains.sort_values(by='rank', inplace=True, ascending=False)

        return predicted_chains


    def get_user_recommendations(self, user_id, limit=15, filter_products=[]):
        """Возвращает рекомендации пользователя"""
        # словарь айди с предиктом модели, уже сортированный по убыванию важности
        model_predictions = self._model_wrapper.predict(user_id)

        if len(model_predictions)>0:
            #Отбираю чейны по фильтру
            filtered_chains = self._chains_dim\
                .loc[(self._chains_dim['default_product_group_id'].isin(filter_products))
                        |
                     (len(filter_products) == 0)
                ]
            #отбираю про предиктам
            predicted_chains = self.__enrich_predictions(model_predictions, filtered_chains)

            # отрезаю по лимиту
            predicted_chains = predicted_chains.head(limit)

            # в дикт
            result = predicted_chains.to_dict(orient='records')
            return result
        return None

    def get_user_history(self, user_id, limit=7):
        """Возвращает историю пользователя"""
        #result = self._chains_dim.sample(limit).to_dict(orient='records')

        user_hist = self._history.loc[self._history['customer_id']==user_id]
        result = pd.merge(user_hist, self._chains_dim, on=['chain_id'])[['chain_id', 'chain_name']].head(limit).to_dict(orient='records')
        #result = user_hist.join(self._chains_dim, on=['chain_id'], lsuffix='hist_')[['chain_id', 'chain_name']].to_dict(orient='records')

        return result

    def get_roller_recommendations(self, selected_restaurants):

        model_predictions = self._model_wrapper.predict_by_roller(selected_restaurants)
        # Имена выбранных  в роллере
        selected_restaurants_names = \
            self._chains_dim.loc[self._chains_dim['chain_id'].isin(selected_restaurants), 'chain_name'].values

        # отбираю про предиктам
        predicted_chains = self.__enrich_predictions(model_predictions, self._chains_dim)

        # не показываю тех, кто был в списке выбранных
        predicted_chains = predicted_chains.loc[~predicted_chains['chain_name'].isin(selected_restaurants_names)]

        # в дикт
        result = predicted_chains.to_dict(orient='records')
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
        """Возвращает список проудктов"""
        return self._products_dim


class RestaurantInfo(dict):
    def __init__(self):
        pass

    def __getattr__(self, attr):
        return self[attr]
