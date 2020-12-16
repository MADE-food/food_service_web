import flask
from flask import jsonify, request, render_template
from core.provider import Provider

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    product_ids = DATA_PROVIDER.get_product_ids()

    if request.method == 'POST':
        try:
            if request.form['user_id']:
                user_id = int(request.form['user_id'])
            else:
                user_id = int(request.form['user_id_dd'])
            prod_ids = [int(i) for i in request.form.getlist('prod_ids[]')]

        except:
            user_id = None
            prod_ids = product_ids

        recom = DATA_PROVIDER.get_user_recommendations(user_id, filter_products = prod_ids)
        hist = DATA_PROVIDER.get_user_history(user_id)
        user_info = {'user_id': user_id}

        data = {
            'history': hist,
            'recommendations': recom,
            'user': user_info
        }
    else:
        data = None
    return render_template('main.html', data=data, product_ids=product_ids)

@app.route('/roller', methods=['GET', 'POST'])
def roller():
    if request.method == 'GET':
        return render_template('roller.html')
    else:
        selected_restaurants = list(request.form.keys())
        selected_restaurants = [int(sr) for sr in selected_restaurants]
        recommendations = DATA_PROVIDER.get_roller_recommendations(selected_restaurants)

        data = {
            'recommendations': recommendations
        }

        return render_template('roller.html', data = data)

@app.route('/about', methods=['GET'])
def about():
    return render_template('team.html')


@app.route('/task', methods=['GET'])
def task():
    return render_template('task.html')

@app.route('/api', methods=['GET'])
def api():
    return render_template('api.html')

# region API
@app.route('/api/v1/recommendations/get', methods=['GET'])
def api_get_recommendations():
    # парсим аргументы запроса
    args = request.args
    user_id = int(args['user_id'])

    # Собираем ответ
    user_info = {'user_id': user_id}
    recommendations = DATA_PROVIDER.get_user_recommendations(user_id)
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
