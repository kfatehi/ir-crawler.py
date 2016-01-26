'''
@Author: Rohan Achar ra.rohan@gmail.com
'''
import re
import time

try:
    # For python 2
    from urlparse import urlparse, parse_qs
except ImportError:
    # For python 3
    from urllib.parse import urlparse, parse_qs

from Crawler4py.Config import Config

class SampleConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.UserAgentString = "UCI Inf141-CS121 crawler 63393716 32393047 22863530 82181685"
        self.PolitenessDelay = 600
        self.MaxQueueSize = 100

    def GetSeeds(self):
        '''Returns the first set of urls to start crawling from'''
        return ["http://www.ics.uci.edu/"]

    def HandleData(self, parsedData):
        '''Function to handle url data. Guaranteed to be Thread safe.
        parsedData = {"url" : "url", "text" : "text data from html", "html" : "raw html data"}
        Advisable to make this function light. Data can be massaged later. Storing data probably is more important'''
        print(time.ctime()+" "+parsedData["url"])
        return

    def ValidUrl(self, url):
        '''Function to determine if the url is a valid url that should be fetched or not.'''
        parsed = urlparse(url)
        valid = False
        try:
            valid =  ".ics.uci.edu" in parsed.hostname \
                and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
			    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
			    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
			    + "|thmx|mso|arff|rtf|jar|csv"\
			    + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        except TypeError:
            print ("TypeError for ", parsed)

        if len(parsed.query) > 0:
            valid = False
            print(time.ctime()+" "+"Rejected QueryString URL: "+url)

        return valid
