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

import NetShelve

class CrawlerConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.UserAgentString = "UCI Inf141-CS121 crawler 63393716 32393047 22863530 82181685"
        self.PolitenessDelay = 600

        #Timeout(Seconds) for trying to get the next url from the frontier. 
        self.FrontierTimeOut = 120

        #Timeout(Seconds) for trying to get a free worker thread, (worker is taking too long maybe?)
        self.WorkerTimeOut = 120

        #Timeout(Seconds) for getting data from the output queue
        self.OutBufferTimeOut = 120

        self.MaxQueueSize = 200

        self.urlValidator = UrlValidator()
        self.dbConf = open('db.conf').read()
        self.connectDatabase()
        print "Using Postgres shelve implementation..."
        self.PersistenceObject = NetShelve.PgShelve(self.conn)

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
            self.conn.rollback()
            url = str(parsedData["url"])
            text = str(parsedData["text"].encode('utf-8'))
            cur = self.conn.cursor()
            query = cur.mogrify("UPDATE PAGES SET TEXT = %s WHERE URL = %s", (text, url))
            cur.execute(query)
            self.conn.commit()
            print "Saved data: "+parsedData["url"]
        except psycopg2.IntegrityError:
            self.conn.rollback()
        except psycopg2.InterfaceError:
            print "Connection reset"
            self.connectDatabase()
        except Exception:
            print "Error saving URL: "+url
            traceback.print_exc()
            try:
                self.conn.rollback()
                print "Rolled back transaction"
            except Exception:
                print "Failed to rollback transaction"

    def ValidUrl(self, url):
        '''Function to determine if the url is a valid url that should be fetched or not.'''
        return self.urlValidator.allows(url)

crawler = Crawler(CrawlerConfig())

print (crawler.StartCrawling())

exit(0)
