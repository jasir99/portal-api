import pyrebase
config = {
    "apiKey": "AIzaSyDc1_MAbRXEA5W_TG20l6fFWQmf0eEFHvk",
    "authDomain": "portal-3229.firebaseapp.com",
    "databaseURL": "https://portal-3229.firebaseio.com",
    "projectId": "portal-3229",
    "storageBucket": "",
    "messagingSenderId": "776604694112",
    "appId": "1:776604694112:web:55a8efc633967600"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

def readNews(col, limit=32):
    newsList = []
    news = db.child(col).order_by_child("published_at").limit_to_last(limit).get().each()
    if news is not None:
        newsList = [n.val() for n in news]
        newsList.reverse()
        return newsList

    return {"message": "No news found!"}

def readNewsByCategory(col, limit, category, _limit=0, newsList=[]):
    _limit = _limit + 10
    news = db.child(col).order_by_child("published_at").limit_to_last(_limit).get().each()[:_limit]
    news.reverse()
    for n in news:
        if n.val()["category"] == category and n.val() not in newsList:
            newsList.append(n.val())
        if len(newsList) == limit:
            return newsList

    return readNewsByCategory(col, limit, category, _limit, newsList)

def readNewsByCategoryV2(col, limit, category):
    i = 0
    _limit = limit
    newsList = []
    news = db.child(col).order_by_child("published_at").limit_to_last(limit).get().each()
    news.reverse()
    for n in news:
        if i == limit:
            return newsList
        if n.val()["category"].lower():
            i += 1
            newsList.append(n.val())
        if n == news[-1] and i < limit:
            _limit += 10
            news1 = db.child(col).order_by_child("published_at").limit_to_last(_limit).get().each()[:10]
            news1.reverse()
            news += news1
