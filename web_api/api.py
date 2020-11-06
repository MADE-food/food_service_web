import flask
from flask import jsonify, request
from core.provider import Provider

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Web API выпускного проекта"


@app.route('/api/v1/recommendations/get', methods=['GET'])
def get_recommendations():
    # парсим аргументы запроса
    args = request.args
    user_id = int(args['user_id'])

    # Собираем ответ
    user_info = {'user_id': user_id}
    recommendations = DATA_PROVIDER.get_user_recomendations(user_id)
    response = {"user": user_info, "recommendations": recommendations}

    return make_response(response, 200)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>This API method does not exist.</p>", 404


def make_response(response_object, code):
    return jsonify(response_object), code


DATA_PROVIDER = Provider()
app.run()
