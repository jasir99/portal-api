import scrapy
import time
from scrapy.crawler import CrawlerProcess
from modules.NewsUtils import getTimeStamp
from modules.models import News
from modules.sqlAlchemy import writeNews


class Telegrafi(scrapy.Spider):
    name = 'Telegrafi'
    base_urls = ["https://telegrafi.com/teknologji/", "https://telegrafi.com/category/lajme/kosove/", "https://telegrafi.com/category/lajme/shqiperi/", "https://telegrafi.com/category/lajme/maqedoni/", "https://telegrafi.com/sport/", "https://telegrafi.com/category/lajme/bote/"]
    def __init__(self):
        self.start_urls = self.base_urls

    def parse(self, response):
        category, country = self._getCategory(response)
        xpath = self._getXpath(category)
        for url in response.xpath(xpath).getall():
            if "category" not in url and "tag" not in url and "ekip" not in url:
                request = scrapy.Request(url, callback=self.parseNews, dont_filter=True)
                request.meta["country"] = country
                request.meta["category"] = category
                yield request

    def parseNews(self, response):
        title = response.xpath("//h1/text()").extract_first()
        image = response.xpath("//figure/img/@src").extract_first()
        link = response.url
        category = response.meta["category"]
        published_at = response.xpath("//div[@class='article-posted']/text()").extract_first().replace("•", "").split("/")[0].strip()
        try:
            published_at = getTimeStamp(published_at, "%d.%m.%Y  %H:%M")
        except:
            _time = int(''.join(c for c in published_at if c.isdigit()))
            if "min" in published_at:
                _time = _time * 60
            else:
                _time = _time * 3600

            published_at = time.time() - _time
        try:
            description = response.xpath("//div[@class='article-body']/p[1]//text()").extract_first()[0:180] + "..."
        except:
            description = "No description available. Click to read more..."
        country = response.meta["country"]
        article = News(title, category, link, description, "Telegrafi", image, published_at, country)
        writeNews(article.serialize)

    def _getXpath(self, category):
        if category == "teknologji":
            return "//div[@class='container teknologji-widget']//a/@href"
        if category == "sport":
            return "//div[@class='container sport-widget']//a/@href"
        return "//div[@class='row cat-list']/div/a/@href"

    def _getCategory(self, response):
        if "teknologji" in str(response):
            return "teknologji", "NA"
        elif "sport" in str(response):
            return "sport", "NA"
        elif "kosove" in str(response):
            return "aktualitet", "KS"
        elif "shqip" in str(response):
            return "aktualitet", "AL"
        elif "bote" in str(response):
            return "aktualitet", "bota"
        else:
            return "aktualitet", "MK"

def telegrafi(r):
    process = CrawlerProcess()
    process.crawl(Telegrafi)
    process.start()

telegrafi(1)