import flask
from flask import jsonify, request, render_template
from core.provider import Provider

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
        except:
            user_id = None

        recom = DATA_PROVIDER.get_user_recomendations(user_id)
        hist = DATA_PROVIDER.get_user_history(user_id)
        user_info = {'user_id': user_id}

        data = {
            'history': hist,
            'recommendations': recom,
            'user': user_info
        }
    else:
        data = None
    return render_template('main.html', data=data)


@app.route('/about', methods=['GET'])
def about():
    return render_template('team.html')


@app.route('/task', methods=['GET'])
def task():
    return render_template('task.html')


# region API
@app.route('/api/v1/recommendations/get', methods=['GET'])
def api_get_recommendations():
    # парсим аргументы запроса
    args = request.args
    user_id = int(args['user_id'])

    # Собираем ответ
    user_info = {'user_id': user_id}
    recommendations = DATA_PROVIDER.get_user_recomendations(user_id)
    response = {"user": user_info, "recommendations": recommendations}

    return make_api_response(response, 200)


@app.route('/api/v1/restaurant/<restaurant_id>', methods=['GET'])
def api_get_restaurant_info(restaurant_id):
    print(restaurant_id)
    resp = DATA_PROVIDER.get_restaraunt_info(restaurant_id)
    return make_api_response(resp, 200)


def make_api_response(response_object, code):
    return jsonify(response_object), code


# endregion

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>This API method does not exist.</p>", 404


DATA_PROVIDER = Provider()
if __name__ == '__main__':
    app.run(debug=True)
