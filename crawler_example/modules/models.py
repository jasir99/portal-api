from datetime import datetime
from hashlib import sha224
from modules.NewsUtils import translateString

class News:
    def __init__(self, title, category, link, description, source, image, published_at, country="NA"):
        self.title = title
        self.category = category
        self.link = link
        self.description = description
        self.source = source
        self.image = image
        self.published_at = datetime.utcfromtimestamp(int(published_at))
        self.crawled_time = datetime.utcnow()
        self.hash = sha224(translateString(link)).hexdigest()
        self.country = country

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
