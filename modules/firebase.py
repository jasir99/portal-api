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

def readNews(news, limit=32, category=""):
    newsList = []
    i = 0
    if db.child(news).get().each() is not None:
        for n in db.child(news).get().each():
            if category != "":
                if n.val()["category"].lower() == category:
                    newsList.append(n.val())
                    i+=1
            else:
                newsList.append(n.val())
                i+=1

        newsList = sorted(newsList, key=lambda k: k['published_at'], reverse=True)
        if limit < len(newsList):
            return newsList[:limit]
        return newsList
    return {"message": "No news found!"}
