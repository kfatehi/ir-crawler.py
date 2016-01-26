'''
@Author: Rohan Achar ra.rohan@gmail.com
'''

import sys
sys.path.append("crawler4py")

from Crawler4py.Crawler import Crawler
from SampleConfig import SampleConfig

crawler = Crawler(SampleConfig())

print (crawler.StartCrawling())

exit(0)
