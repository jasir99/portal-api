from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
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


def writeNews(news):
    n = News(title=news['title'], category=news['category'], link=news['link'],
             description=news['description'], source=news['source'], image=news['image'],
             published_at=news['published_at'], crawled_time=news['crawled_time'],
             hash=news['hash'], country=news['country'])
    db.session.add(n)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
