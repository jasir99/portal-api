from flask import Flask, request, jsonify
from modules.firebase import readNews
from flask_cors import CORS


API_KEY = "f3761fb8-cd8c-4e1b-be62-382a3f654513"

app = Flask(__name__)
CORS(app)


def toInt(tmpVal, default=0):
    if tmpVal is None or not tmpVal.isdigit:
        return default
    else:
        return int(tmpVal)

@app.route("/", methods=['GET'])
def news_all():
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('offset'), 32)
    startAt = toIng(request.args.get("startAt"), 0)
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})

    news = readNews("portal", limit)[startAt:]
    return jsonify(total=len(news), news=news)


@app.route("/<category>")
def news_category(category):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get('offset'), 0)

    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})

    news = sorted(readNews("portal", limit, category), key=lambda k: k['published_at'], reverse=True)
    return jsonify(total=len(news), news=news)
