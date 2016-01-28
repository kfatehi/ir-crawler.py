from urlparse import urlparse, parse_qs
import re

class UrlValidator():
    def allows(self, url):
        parsed = urlparse(url)
        valid = False
        try:
            valid = self.isICS(parsed.hostname) and not self.isBadType(parsed.path)
            if valid and len(parsed.query) > 0:
                self.isAllowedQuery(parsed.query)
                valid = False
        except TypeError:
            print ("TypeError for ", parsed)
        return valid

    def isBadType(self, path):
        return re.match(".*\.(css|js|bmp|gif|jpe?g|ico|svg" \
                + "|png|tiff?|mid|mp2|mp3|mp4" \
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                + "|thmx|mso|arff|rtf|jar|csv"\
                + "|java|war|sh|cc|cpp|h|xml|rss|r"\
                + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", path.lower())

    def isICS(self, hostname):
        return ".ics.uci.edu" in hostname

    def isAllowedQuery(self, query):
        if query == 'rsd': return False
        qs = parse_qs(query)
        if 'action' in qs:
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

# run it with `make test-whitelist`
if __name__ == "__main__":
    uv = UrlValidator()
    import fileinput
    for line in fileinput.input():
        try:
            url = line.split("URL: ")[1].strip()
            parsed = urlparse(url)
            if uv.isICS(parsed.hostname) and not uv.isBadType(parsed.path) and len(parsed.query) > 0:
                if uv.isAllowedQuery(parsed.query):
                    print "Allow: "+url
                    pass
                else:
                    #print "Reject: "+url
                    pass
        except IndexError:
            pass
