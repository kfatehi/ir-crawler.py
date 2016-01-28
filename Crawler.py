import sys
sys.path.append("crawler4py")
from Crawler4py.Crawler import Crawler
from Crawler4py.Config import Config
from urlparse import urlparse, parse_qs
import re
import time
from UrlValidator import UrlValidator

class CrawlerConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.UserAgentString = "UCI Inf141-CS121 crawler 63393716 32393047 22863530 82181685"
        self.PolitenessDelay = 600
        self.MaxQueueSize = 100
        # lower number makes it exit faster after interrupt
        self.OutBufferTimeOut = 10
        self.urlValidator = UrlValidator()

    def GetSeeds(self):
        '''Returns the first set of urls to start crawling from'''
        return ["http://www.ics.uci.edu/"]

    def HandleData(self, parsedData):
        '''Function to handle url data. Guaranteed to be Thread safe.
        parsedData = {"url" : "url", "text" : "text data from html", "html" : "raw html data"}
        Advisable to make this function light. Data can be massaged later. Storing data probably is more important'''
        print(time.ctime()+" "+parsedData["url"])

    def ValidUrl(self, url):
        '''Function to determine if the url is a valid url that should be fetched or not.'''
        return self.urlValidator.allows(url)

crawler = Crawler(CrawlerConfig())

print (crawler.StartCrawling())

exit(0)
