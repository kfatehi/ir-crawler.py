from urlparse import urlparse, parse_qs
import re

class UrlValidator():
    def __init__(self, verbose=False):
        self.verbose = verbose

    def allows(self, url):
        parsed = urlparse(url)
        path = parsed.path.lower()
        try:
            if not self.isICS(parsed.hostname):
                self.feedback("Reject, not ICS "+url)
                return False
            if self.isBadPath(parsed.path):
                self.feedback("Reject, bad path "+url)
                return False
            if self.isBadType(parsed.path):
                self.feedback("Reject, bad type "+url)
                return False
            if not self.isAllowedQuery(url, parsed.query):
                self.feedback("Reject, bad query string "+url)
                return False
            if not self.isAllowedFragment(parsed.fragment):
                self.feedback("Reject, bad fragment "+url)
                return False
            self.feedback("Allow "+url)
            return True
        except TypeError:
            print ("TypeError for ", parsed)
            return False

    def feedback(self, string):
        if self.verbose:
            print string

    def isBadPath(self, path):
        if "/pub/arch/adl/adl/" in path: return True
        if "<a href=" in path: return True
        if "datasets/datasets/datasets" in path: return True
        return False

    def isAllowedFragment(self, frag):
        if re.match(".*respond.*", frag): return False
        return True

    def isBadType(self, path):
        return re.match(".*\.(css|js|bmp|gif|jpe?g|ico|svg" \
                + "|png|tiff?|mid|mp2|mp3|mp4" \
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                + "|thmx|mso|arff|rtf|jar|csv"\
                + "|java|war|sh|cc|cpp|h|xml|rss|r"\
                + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", path)

    def isICS(self, hostname):
        return ".ics.uci.edu" in hostname

    def isAllowedQuery(self, url, query):
        if query.strip() == 'rsd': return False
        qs = parse_qs(query)
        # Block all query string urls downstream of datasets
        if "archive.ics.uci.edu/ml/datasets.html?" in url:
            return False
        # Block this messed up wiki
        if "ironwood.ics.uci.edu/lib/exe/indexer.php?" in url:
            return False
        if 'replytocom' in qs: return False
        if 'action' in qs:
            if qs['action'] == 'download': return False
            if qs['action'] == 'upload': return False
            if qs['action'][0] == 'download': return False
            if qs['action'][0] == 'upload': return False
        # we wont block the calendar outright, but:
        if 'calendar' in qs:
            # you can have different calendar view types, block them all
            if 'fromDate' in qs: return False
            if 'day' in qs: return False
            if 'month' in qs: return False
            if 'year' in qs: return False
        if 'url' in qs: return False
        if 'rsd' in qs: return False
        # Some kind of timeline we cant access anyway...
        if 'from' in qs and 'precision' in qs: return False
        return True

# the rest is just for testing ...

def test_logfile():
    uv = UrlValidator(verbose=True)
    import fileinput
    for line in fileinput.input():
        try:
            url = line.split("Fetching ")[1].strip()
            uv.allows(url)
        except IndexError:
            pass

def test_direct():
    uv = UrlValidator(verbose=True)
    import fileinput
    for url in fileinput.input():
        uv.allows(url)

if __name__ == "__main__":
    #test_logfile();
    test_direct();
