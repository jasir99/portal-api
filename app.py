from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


API_KEY = "f3761fb8-cd8c-4e1b-be62-382a3f654513"
app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jasir123@localhost:5432/NewsAPI'
db = SQLAlchemy(app)


class News(db.Model):
    title = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    link = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    source = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=True)
    published_at = db.Column(db.DateTime(timezone=True), nullable=True)
    crawled_time = db.Column(db.DateTime(timezone=True), nullable=True)
    hash = db.Column(db.String(), nullable=False, primary_key=True)
    country = db.Column(db.String(), nullable=True)

    @property
    def serialize(self):
        return {
            'title': self.title,
            'category': self.category,
            'link': self.link,
            'description': self.description,
            'source': self.source,
            'image': self.image,
            'country': self.country,
            'published_at': self.published_at,
            'crawled_time': self.crawled_time,
            'hash': self.hash
        }



def toInt(tmpVal, default=0):
    if tmpVal is None or not tmpVal.isdigit:
        return default
    else:
        return int(tmpVal)


def getNews(limit, offset):
    news = News.query.order_by(News.published_at.desc()).paginate(page=offset, per_page=limit).items
    n_list = []
    for n in news:
        n_list.append(n.serialize)
    return n_list

@app.route("/", methods=['GET'])
def news_all():
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 1)
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = getNews(limit, offset)
    return jsonify(total=len(news), news=news)


def getNewsByCategory(limit, offset, category):
    news = News.query.filter_by(category=category).order_by(News.published_at.desc()).paginate(page=offset, per_page=limit).items
    n_list = []
    for n in news:
        n_list.append(n.serialize)
    return n_list

@app.route("/<category>")
def news_category(category):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 1)
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = getNewsByCategory(limit, offset, category)
    return jsonify(total=len(news), news=news)


def getNewsByCountry(limit, offset, country):
    news = News.query.filter_by(country=country).order_by(News.published_at.desc()).paginate(page=offset, per_page=limit).items
    n_list = []
    for n in news:
        n_list.append(n.serialize)
    return n_list

@app.route("/aktualitet/<country>")
def news_country(country):
    api_key = request.args.get("api_key")
    limit = toInt(request.args.get('limit'), 10)
    offset = toInt(request.args.get("offset"), 1)
    if api_key != API_KEY:
        return jsonify({"message": "Bad API Key!"})
    news = getNewsByCountry(limit, offset, country)
    return jsonify(total=len(news), news=news)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3005, debug=True)
