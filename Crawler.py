import sys
sys.path.append("crawler4py")
sys.path.append("psycopg2-2.6.1")
from Crawler4py.Crawler import Crawler
from Crawler4py.Config import Config
from urlparse import urlparse, parse_qs
import re
from UrlValidator import UrlValidator

import psycopg2
import traceback

class CrawlerConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.UserAgentString = "UCI Inf141-CS121 crawler 63393716 32393047 22863530 82181685"
        self.PolitenessDelay = 600
        self.MaxQueueSize = 100
        self.urlValidator = UrlValidator()
        self.dbConf = open('db.conf').read()
        self.connectDatabase()

    def connectDatabase(self):
        try:
            self.conn = psycopg2.connect(self.dbConf)
            print "Connected to database..."
        except Exception:
            traceback.print_exc()
            print "Could not connect to database, exiting."
            print "Please close manually if it doesn't exit..."
            sys.exit(1)

    def GetSeeds(self):
        '''Returns the first set of urls to start crawling from'''
        return ["http://www.ics.uci.edu/"]

    def HandleData(self, parsedData):
        '''Function to handle url data. Guaranteed to be Thread safe.
        parsedData = {"url" : "url", "text" : "text data from html", "html" : "raw html data"}
        Advisable to make this function light. Data can be massaged later. Storing data probably is more important'''
        try:
            url = str(parsedData["url"])
            text = str(parsedData["text"].encode('utf-8'))
            cur = self.conn.cursor()
            values = (url, text)
            query = cur.mogrify("INSERT INTO PAGES (URL, TEXT) VALUES (%s, %s)", values)
            cur.execute(query)
            self.conn.commit()
            print "Saved data: "+parsedData["url"]
        except psycopg2.IntegrityError:
            print "Already saved "+url
            self.conn.rollback()
        except psycopg2.InterfaceError:
            print "Connection reset"
            self.connectDatabase()
        except Exception:
            print "Error saving URL: "+url
            traceback.print_exc()

    def ValidUrl(self, url):
        '''Function to determine if the url is a valid url that should be fetched or not.'''
        return self.urlValidator.allows(url)

crawler = Crawler(CrawlerConfig())

print (crawler.StartCrawling())

exit(0)
