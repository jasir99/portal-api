import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./serviceaccount.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def getNews(limit, category=""):
    news_ref = db.collection("portal")
    sport_news = []
    if category != "":
        sport_news = news_ref.where('category', '==', category).order_by('published_at', direction=firestore.Query.DESCENDING).limit(limit).stream()
    else:
        sport_news = news_ref.order_by('published_at', direction=firestore.Query.DESCENDING).limit(limit).stream()
    sport_news = [n.to_dict() for n in sport_news]
    return sport_news
