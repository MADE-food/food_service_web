class Provider():
    def __init__(self):
        pass

    def get_user_recomendations(self, user_id):
        """Возвращает рекомендации пользователя"""
        tmp_recomendations = {
            1: [{"id": 1,
                 "image": "/images/img1.png",
                 "name": 'Restaurant 1',
                 "rank": 1},
                {"id": 2,
                 "image": "/images/img2.png",
                 "name": 'Restaurant 2',
                 "rank": 2}],
            2: [{"id": 3,
                 "image": "/images/img3.png",
                 "name": 'Restaurant 3',
                 "rank": 2},
                {"id": 4,
                 "image": "/images/img4.png",
                 "name": 'Restaurant 4',
                 "rank": 1}]
        }

        return tmp_recomendations.get(user_id, [])

    def get_user_history(self, user_id):
        """Возвращает рекомендации пользователя"""
        tmp_recomendations = {
            1: [{"id": 3,
                 "image": "/images/img3.png",
                 "name": 'Restaurant 3',
                 "rank": 2},
                {"id": 4,
                 "image": "/images/img4.png",
                 "name": 'Restaurant 4',
                 "rank": 1}],
            2: [{"id": 1,
                 "image": "/images/img1.png",
                 "name": 'Restaurant 1',
                 "rank": 1},
                {"id": 2,
                 "image": "/images/img2.png",
                 "name": 'Restaurant 2',
                 "rank": 2}]
        }

        return tmp_recomendations.get(user_id, [])

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
