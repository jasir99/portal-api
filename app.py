from flask import Flask, request, jsonify
from modules.firestore import getNews, getNewsByCategory, getNewsByCountry
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
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 0)
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = getNews(limit, limit*offset)
    return jsonify(total=len(news), news=news)

@app.route("/<category>")
def news_category(category):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 0)
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = getNewsByCategory(limit, limit*offset, category)
    return jsonify(total=len(news), news=news)

@app.route("/aktualitet/<country>")
def news_country(country):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 0)
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    startAt = limit*offset
    news = getNewsByCountry(limit, limit*offset, country)
    return jsonify(total=len(news), news=news)
