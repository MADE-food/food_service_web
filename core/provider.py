import json

class Provider():
    def __init__(self):
        with open("core/data.json", 'r') as f:
            self._data = json.load(f)

    def get_user_recomendations(self, user_id):
        """Возвращает рекомендации пользователя"""
        result = self._data['tmp_recomendations'].get(str(user_id), [])
        return result

    def get_user_history(self, user_id):
        """Возвращает историю пользователя"""
        result = self._data['tmp_history'].get(str(user_id), [])
        return result

    def get_restaraunt_info(self, restaurant_id):
        """Возвращает информацию по выбранному ресторану"""
        tmp_rest_info = {
            "1": {
                "id": restaurant_id,
                "name": "Rest 1",
                "description": "Rest 1 description",
            }
        }
        return tmp_rest_info.get(restaurant_id, None)
