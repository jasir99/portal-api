import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./serviceaccount.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def getNews(limit, offset):
    news_ref = db.collection("portal")
    news = news_ref.order_by('published_at', direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()
    news = [n.to_dict() for n in news]
    return news

def getNewsByCategory(limit, offset, category):
    news_ref = db.collection("portal")
    news = news_ref.where('category', '==', category).order_by('published_at', direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()
    news = [n.to_dict() for n in news]
    return news

def getNewsByCountry(limit, offset, country):
    news_ref = db.collection("portal")
    news = news_ref.where('country', '==', country.upper()).order_by('published_at', direction=firestore.Query.DESCENDING).limit(limit).offset(offset).stream()
    news = [n.to_dict() for n in news]
    return news
